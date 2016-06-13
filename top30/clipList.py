from PyQt4 import QtCore, QtGui, uic

class ClipListModel(QtCore.QAbstractTableModel):
    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self, parent=None)
        self.setSupportedDragActions(QtCore.Qt.MoveAction)
        self.horizontal_header = ["Type", "Filename", "Start"]
        self.data = []

    def flags(self, index):
        if index.isValid():
            return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 3

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.data[index.row()][index.column()]
        return None

    def headerData(self, index, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal: 
            return self.horizontal_header[index]
        else:
            return str(index + 1)

    def appendRow(self, row):
        self.insertRows(self.rowCount(),[row])

    def insertRows(self, row, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row + len(rows) - 1)
        for i in range(len(rows)):
            row_i = row + i
            self.data.insert(row_i, rows[i])
        self.endInsertRows()

    def insertRow(self, row, row_data):
        self.insertRows(row, [row_data])

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            del self.data[row + count - 1]
        self.endRemoveRows()
        return True

    def removeRow(self, row):
        self.removeRows(row, 1)

    def moveRows(self, source_parent, source_first, source_last, 
            destination_parent, destination):
# Handle funny crashing bug
        self.beginMoveRows(source_parent, source_first, source_last, 
                destination_parent, destination)
        items = self.data[source_first:source_last + 1]
        self.data = self.data[:source_first] + self.data[source_last + 1:]
        for i in range(len(items)):
            self.data.insert(destination + i, items[i])
        self.endMoveRows()

class ClipListView(QtGui.QTableView):
    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent=None)
        self.horizontalHeader().setStretchLastSection(True)
        self.resizeColumnsToContents()
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/top30clip') or event.mimeData().hasFormat('audion/ogg') or event.mimeData().hasFormat('audion/mp3'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid() or index.row() == self.source_index.row():
            return
        source = self.source_index.row()
        destination = index.row()
        if destination == source + 1:
            destination = source
            source += 1
        self.model().moveRows(QtCore.QModelIndex(), source, source, 
                QtCore.QModelIndex(), destination)
        event.accept()

    def mousePressEvent(self, event):
        super(ClipListView, self).mousePressEvent(event)
        self.startDrag(event)

    def startDrag(self, event):
        self.source_index = self.indexAt(event.pos())
        if not self.source_index.isValid():
            return

        drag = QtGui.QDrag(self)

        mimeData = QtCore.QMimeData()
        mimeData.setData("application/top30clip", "")
        drag.setMimeData(mimeData)

        vis = self.source_index.sibling(self.source_index.row() + 1, self.source_index.column())
        pixmap = QtGui.QPixmap()
        pixmap = pixmap.grabWidget(self, self.visualRect(vis))
        drag.setPixmap(pixmap)
        result = drag.start(QtCore.Qt.MoveAction)
