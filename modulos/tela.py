from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys


class UI_feedback(object):
    def setupUi(self, feedback):
        if not feedback.objectName():
            feedback.setObjectName(u"feedback")
        feedback.resize(653, 222)
        feedback.setMinimumSize(QSize(653, 222))
        feedback.setMaximumSize(QSize(653, 222))
        self.centralwidget = QWidget(feedback)
        self.centralwidget.setObjectName(u"centralwidget")
        self.enviar = QPushButton(self.centralwidget)
        self.enviar.setObjectName(u"enviar")
        self.enviar.setGeometry(QRect(510, 120, 111, 51))
        font = QFont()
        font.setPointSize(12)
        self.enviar.setFont(font)
        self.enviar.setStyleSheet(u"border-radius: 10px;\n"
                                  "background-color: rgb(255, 255, 255);")
        self.mensagem = QLineEdit(self.centralwidget)
        self.mensagem.setObjectName(u"mensagem")
        self.mensagem.setGeometry(QRect(30, 40, 591, 51))
        self.mensagem.setFont(font)
        feedback.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(feedback)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 653, 26))
        feedback.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(feedback)
        self.statusbar.setObjectName(u"statusbar")
        feedback.setStatusBar(self.statusbar)

        self.retranslateUi(feedback)

        QMetaObject.connectSlotsByName(feedback)

    # setupUi

    def retranslateUi(self, feedback):
        feedback.setWindowTitle(QCoreApplication.translate("feedback", u"Feedback", None))
        self.enviar.setText(QCoreApplication.translate("feedback", u"Enviar", None))
    # retranslateUi


if __name__ == "__main__":
    a = QApplication(sys.argv)
    j = UI_feedback()
    sys.exit(a.exec_())
