# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Ui_Ancfcc
                                 A QGIS plugin

 this is an experimental test version of this plugin
                             -------------------
        begin                : 2020-02-04
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Ancfcc
        email                : ilyasbenhssine@gmail.com
 ***************************************************************************/
"""

import os
import psycopg2

# from qgis.PyQt import uic
# from qgis.PyQt import QtWidgets, QtGui
from PyQt5 import QtCore, QtGui, QtWidgets, uic, Qt
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.utils import iface
from qgis.core import QgsPointXY, QgsPoint, QgsGeometry, QgsWkbTypes

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'anfcc_test_dialog_base.ui'))


class Ui_Ancfcc(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Ui_Ancfcc, self).__init__(parent)

        self.setupUi(self)
        print("'--- ANCFCC PLUGIN STARTED'")

        try:
            conn =  psycopg2.connect("dbname='postgres' user='postgres' password='123'")
            print("'--INFO--' : Connected to database")
        except:
            print("'--ERROR--' : Error while connecting to database.")

        cur = conn.cursor()
        try:
            self.comboBoxNature.addItem("T")
            self.comboBoxNature.addItem("R")

            cur.execute("""Select type from public.type""")
            rslt = cur.fetchall()
            for record in rslt:
                subject_name = "%s" %record
                self.comboBoxType.addItem(subject_name)

            cur.execute("""Select mappe from public.mappe""")
            rslt = cur.fetchall()
            for record in rslt:
                subject_name = "%s" %record
                self.comboBoxMap.addItem(subject_name)
        except:
            print ("'--ERROR--' :  Can't fill combo boxes / Table View.")
        # cur.close()
        # conn.close()

        self.home()

    def home(self):
        reject = self.reject
        reject.clicked.connect(self.close_application)

        addbtn = self.AddButton
        addbtn.clicked.connect(self.addborne)

        delbtn = self.DeleteButton
        delbtn .clicked.connect(self.delrow)

        save = self.accept
        save.clicked.connect(self.save_data)

        tablewidget = self.tableWidgetBornes
        tablewidget.clicked.connect(self.previewpoint)

        cleartitre = self.cleartitlebtn
        cleartitre.clicked.connect(self.cleartitle)

        updatebtn = self.update
        updatebtn.clicked.connect(self.updateall)




    def cleartitle(self):
        self.lineEditNum.setText("")
        self.lineEditIndice.setText("")


    def delrow(self):
        ## get selected row
        rowPos = self.tableWidgetBornes.currentRow()
        self.tableWidgetBornes.removeRow(rowPos)
        rowCnt = self.tableWidgetBornes.rowCount()
        self.spinBoxnb_bornes.setValue(rowCnt)
        ## delete row
        print("'--INFO--' : ROW DELETED")

    def close_application(self):
        print("'--INFO--' : APP CLOSED")
        self.hide()

    def addborne(self):

        rowPos = self.tableWidgetBornes.rowCount()
        self.tableWidgetBornes.insertRow(rowPos)
        self.spinBoxnb_bornes.setValue(rowPos + 1)

        print("'--INFO--' : Ready to add item")
        # self.mc=iface.mapCanvas()
        # self.canvas =iface.mapCanvas()
        # self.pointTool = QgsMapToolEmitPoint(self.mc)
        # self.mc.setMapTool(self.pointTool)
        # self.result = self.pointTool.canvasClicked.connect(self.display_point)
        # self.listFeat=[]
        # self.rubberBand = QgsRubberBand(self.canvas , QgsWkbTypes.PointGeometry)
        # self.rubberBand.setColor(Qt.red)
        # self.rubberBand.setIcon(QgsRubberBand.IconType.ICON_CIRCLE)
        # self.rubberBand.setIconSize(19)
        # itemnom = QtWidgets.QTableWidgetItem("nom")
        # posX = self.result.x
        # posY = self.result.y
        # itemx = QtWidgets.QTableWidgetItem(posX)
        # itemy = QtWidgets.QTableWidgetItem(posY)
        # self.tableWidgetBornes.setItem(rowPos, 0, itemnom)
        # self.tableWidgetBornes.setItem(rowPos, 1, itemx)
        # self.tableWidgetBornes.setItem(rowPos, 2, itemy)
        # print("'--INFO-- : Item Added'")

    def save_data(self):
        if (self.lineEditNum.text() != ""):
            if (self.lineEditIndice.text() != ""):
                if (self.tableWidgetBornes.rowCount() >= 3):
                    print ("'--INFO--' : Filter working")
                    cmbnature = self.comboBoxNature.currentText()
                    fieldnum = self.lineEditNum.text()
                    fieldindice = self.lineEditIndice.text()
                    typocomb = self.comboBoxType.currentText()
                    nbbornes = self.tableWidgetBornes.rowCount()
                    mapfield = self.comboBoxMap.currentText()
                    titreref = "" + cmbnature + fieldnum + fieldindice
                    conn =  psycopg2.connect("dbname='postgres' user='postgres' password='123'")
                    cur = conn.cursor()
                    sql = ("""INSERT INTO public.titres (nature, num, indice, mappe, type, nb_bornes, titref) VALUES (%s, %s, %s, %s, %s, %s, %s);""")
                    # print(sql)
                    cur.execute(sql, (cmbnature, fieldnum, fieldindice, mapfield, typocomb, nbbornes, titreref))
                    conn.commit()
                    print("'--INFO--' : Data Saved to Database")
                    try:
                        bornes=[]
                        for x in range(0, nbbornes):
                            name = self.tableWidgetBornes.item(x, 0).text()
                            psx = self.tableWidgetBornes.item(x, 1).text()
                            psy = self.tableWidgetBornes.item(x, 2).text()
                            bornes.append(QgsPointXY(float(psx), float(psy)))
                            geometryborne = QgsGeometry.fromPointXY(QgsPointXY(float(psx), float(psy))).asWkt()
                            try:
                                pt = QgsPointXY(float(psx), float(psy))
                                print("'--INFO--': name:"+name+" x:"+psx+" y:"+psy)
                                rb = QgsRubberBand(iface.mapCanvas(), True)
                                rb.reset(QgsWkbTypes.PointGeometry)
                                rb.addPoint(pt)
                                print("'--INFO--':  the born '"+name+"' was added.")
                            except:
                                print("'--INFO--': You need to enter a number not text in X, Y Fields")

                            try:
                                sql = ("INSERT INTO public.bornes (nature, num, indice, name, x, y, titref, the_geom ) VALUES ('"+cmbnature+"', "+fieldnum+", '"+fieldindice+"', '"+name+"', "+psx+", "+psy+", '"+titreref+"', ST_GeomFromText('"+geometryborne+"', 26191))")
                                print(sql)
                                # sql = ("""INSERT INTO public.bornes (nature, num, indice, name, x, y, titref, the_geom ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""")
                                cur = conn.cursor()
                                # cur.execute(sql, (cmbnature, fieldnum, fieldindice, name, psx, psy, titreref, thegeom))
                                cur.execute(sql)
                                conn.commit()
                            except:
                                print("'--ERROR--': Error while sending querry")
                                self.ErrorLabel.setText("Error on Querry")
                    except:
                        print("'--INFO--': PLZ Fill all fields")
                        self.ErrorLabel.setText("Fields empty detected")

                    geometry = QgsGeometry.fromPolygonXY([bornes])
                    geometrypolygon = geometry.asWkt()
                    # thegeomshape = "ST_GeomFromText('"+geometry+"', 26191))
                    
                    try:
                        sql = ("UPDATE public.titres SET the_geom = ST_GeomFromText('"+geometrypolygon+"', 26191) WHERE titref = '"+titreref+"';")
                        print(sql)
                        cur = conn.cursor()
                        cur.execute(sql)
                        conn.commit()
                    except:
                        print ("'--INFO--': Can''t edit titre")
                        self.ErrorLabel.setText("Can't Edit titre")
                else:
                    self.ErrorLabel.setText("Fields empty detected")
            else:
                self.ErrorLabel.setText("Fields empty detected")
        else:
            self.ErrorLabel.setText("Fields empty detected")


    
    def previewpoint(self):
        # empty = QtWidgets.QTableWidgetItem("")
        if self.tableWidgetBornes.item(self.tableWidgetBornes.currentRow(), 0) != None:
            if self.tableWidgetBornes.item(self.tableWidgetBornes.currentRow(), 1) != None:
                if self.tableWidgetBornes.item(self.tableWidgetBornes.currentRow(), 2) != None:
                    
                    fname = self.tableWidgetBornes.item(self.tableWidgetBornes.currentRow(), 0).text()
                    fcasex = self.tableWidgetBornes.item(self.tableWidgetBornes.currentRow(), 1).text()
                    fcasey = self.tableWidgetBornes.item(self.tableWidgetBornes.currentRow(), 2).text()
                    try:
                        pt = QgsPointXY(float(fcasex), float(fcasey))
                        print("'--INFO--': name:"+fname+" x:"+fcasex+" y:"+fcasey)
                        rb = QgsRubberBand(iface.mapCanvas(), True)
                        rb.reset(QgsWkbTypes.PointGeometry)
                        rb.addPoint(pt)
                    except:
                        print("'--INFO--': You need to enter a number not text in X, Y Fields")

                else:
                    print("'---': a field is empty")
            else:
                print("'---': a field is empty")
        else:
            print("'---': a field is empty")

    def showpoints(self, name, x, y):
        try:
            pt = QgsPointXY(float(x), float(y))
            print("'--INFO--': name:"+name+" x:"+x+" y:"+y)
            rb = QgsRubberBand(iface.mapCanvas(), True)
            rb.reset(QgsWkbTypes.PointGeometry)
            rb.addPoint(pt)
        except:
            print("'--ERROR--': Error while Displaying points")

    def updateall(self):
        if (self.lineEditNum.text() != ""):
            if (self.lineEditIndice.text() != ""):
                if (self.tableWidgetBornes.rowCount() >= 3):
                    print("'--INFO--' : Filter Passed Successfully")
                    cmbnature = self.comboBoxNature.currentText()
                    fieldnum = self.lineEditNum.text()
                    fieldindice = self.lineEditIndice.text()
                    typocomb = self.comboBoxType.currentText()
                    nbbornes = self.tableWidgetBornes.rowCount()
                    mapfield = self.comboBoxMap.currentText()
                    titreref = "" + cmbnature + fieldnum + fieldindice
                    conn = psycopg2.connect("dbname='postgres' user='postgres' password='123'")
                    cur = conn.cursor()
                    sql = ("""UPDATE public.titres SET mappe = %s, type = %s, nb_bornes = %s  WHERE titref = %s ;""")
                    # print(sql)
                    cur.execute(sql, (mapfield, typocomb, nbbornes, titreref))
                    conn.commit()
                    print("'--INFO--' : Data Saved to Database")
                    try:
                        bornes = []
                        for x in range(0, nbbornes):
                            name = self.tableWidgetBornes.item(x, 0).text()
                            psx = self.tableWidgetBornes.item(x, 1).text()
                            psy = self.tableWidgetBornes.item(x, 2).text()
                            bornes.append(QgsPointXY(float(psx), float(psy)))
                            geometryborne = QgsGeometry.fromPointXY(QgsPointXY(float(psx), float(psy))).asWkt()
                            try:
                                pt = QgsPointXY(float(psx), float(psy))
                                print("'--INFO--': name:" + name + " x:" + psx + " y:" + psy)
                                rb = QgsRubberBand(iface.mapCanvas(), True)
                                rb.reset(QgsWkbTypes.PointGeometry)
                                rb.addPoint(pt)
                                print("'--INFO--':  the born '" + name + "' was added.")
                            except:
                                print("'--INFO--': You need to enter a number not text in X, Y Fields")

                            try:
                                sql = ("UPDATE public.bornes SET x = "+psx+", y = "+psy+", the_geom = ST_GeomFromText('" + geometryborne + "', 26191) WHERE titref = '"+titreref+"' AND name = '"+name+"';")
                                print(sql)
                                cur = conn.cursor()
                                cur.execute(sql)
                                conn.commit()
                            except:
                                print("'--ERROR--': Error while sending querry")
                                self.ErrorLabel.setText("Error on Querry")
                    except:
                        print("'--INFO--': PLZ Fill all fields")
                        self.ErrorLabel.setText("Fields empty detected")

                    geometry = QgsGeometry.fromPolygonXY([bornes])
                    geometrypolygon = geometry.asWkt()
                    # thegeomshape = "ST_GeomFromText('"+geometry+"', 26191))

                    try:
                        sql = (
                                    "UPDATE public.titres SET the_geom = ST_GeomFromText('" + geometrypolygon + "', 26191) WHERE titref = '" + titreref + "';")
                        print(sql)
                        cur = conn.cursor()
                        cur.execute(sql)
                        conn.commit()
                    except:
                        print("'--INFO--': Can''t edit titre")
                        self.ErrorLabel.setText("Can't Edit titre")
                else:
                    self.ErrorLabel.setText("Bornes < 3")
            else:
                self.ErrorLabel.setText("No Indice detected")
        else:
            self.ErrorLabel.setText("No Number detected")

    def updatetitre(self):
        if (self.lineEditNum.text() != ""):
            if (self.lineEditIndice.text() != ""):
                if (self.tableWidgetBornes.rowCount() >= 3):
                    print("'--INFO--' : Filter Passed Successfully")
                    cmbnature = self.comboBoxNature.currentText()
                    fieldnum = self.lineEditNum.text()
                    fieldindice = self.lineEditIndice.text()
                    typocomb = self.comboBoxType.currentText()
                    nbbornes = self.tableWidgetBornes.rowCount()
                    mapfield = self.comboBoxMap.currentText()
                    titreref = "" + cmbnature + fieldnum + fieldindice
                    conn = psycopg2.connect("dbname='postgres' user='postgres' password='123'")
                    cur = conn.cursor()
                    sql = ("""UPDATE public.titres SET mappe = %s, type = %s, nb_bornes = %s  WHERE titref = %s ;""")
                    # print(sql)
                    cur.execute(sql, (mapfield, typocomb, nbbornes, titreref))
                    conn.commit()
                    print("'--INFO--' : Data Saved to Database")
                else:
                    self.ErrorLabel.setText("Bornes < 3")
            else:
                self.ErrorLabel.setText("No Indice detected")
        else:
            self.ErrorLabel.setText("No Number detected")

    def updateborn(self):
        if (self.lineEditNum.text() != ""):
            if (self.lineEditIndice.text() != ""):
                if (self.tableWidgetBornes.rowCount() >= 3):
                    print("'--INFO--' : Filter Passed Successfully")
                    cmbnature = self.comboBoxNature.currentText()
                    fieldnum = self.lineEditNum.text()
                    fieldindice = self.lineEditIndice.text()
                    typocomb = self.comboBoxType.currentText()
                    nbbornes = self.tableWidgetBornes.rowCount()
                    mapfield = self.comboBoxMap.currentText()
                    titreref = "" + cmbnature + fieldnum + fieldindice
                    conn = psycopg2.connect("dbname='postgres' user='postgres' password='123'")
                    print("'--INFO--' : Data Saved to Database")
                    try:
                        bornes = []
                        for x in range(0, nbbornes):
                            name = self.tableWidgetBornes.item(x, 0).text()
                            psx = self.tableWidgetBornes.item(x, 1).text()
                            psy = self.tableWidgetBornes.item(x, 2).text()
                            bornes.append(QgsPointXY(float(psx), float(psy)))
                            geometryborne = QgsGeometry.fromPointXY(QgsPointXY(float(psx), float(psy))).asWkt()
                            try:
                                pt = QgsPointXY(float(psx), float(psy))
                                print("'--INFO--': name:" + name + " x:" + psx + " y:" + psy)
                                rb = QgsRubberBand(iface.mapCanvas(), True)
                                rb.reset(QgsWkbTypes.PointGeometry)
                                rb.addPoint(pt)
                                print("'--INFO--':  the born '" + name + "' was added.")
                            except:
                                print("'--INFO--': You need to enter a number not text in X, Y Fields")

                            try:
                                sql = ("UPDATE public.bornes SET x = "+psx+", y = "+psy+", the_geom = ST_GeomFromText('" + geometryborne + "', 26191) WHERE titref = '"+titreref+"' AND name = '"+name+"';")
                                print(sql)
                                cur = conn.cursor()
                                cur.execute(sql)
                                conn.commit()
                            except:
                                print("'--ERROR--': Error while sending querry")
                                self.ErrorLabel.setText("Error on Querry")
                    except:
                        print("'--INFO--': PLZ Fill all fields")
                        self.ErrorLabel.setText("Fields empty detected")

                    geometry = QgsGeometry.fromPolygonXY([bornes])
                    geometrypolygon = geometry.asWkt()
                    # thegeomshape = "ST_GeomFromText('"+geometry+"', 26191))

                    try:
                        sql = ("UPDATE public.titres SET the_geom = ST_GeomFromText('" + geometrypolygon + "', 26191) WHERE titref = '" + titreref + "';")
                        print(sql)
                        cur = conn.cursor()
                        cur.execute(sql)
                        conn.commit()
                    except:
                        print("'--INFO--': Can''t edit titre")
                        self.ErrorLabel.setText("Can't Edit titre")
                else:
                    self.ErrorLabel.setText("Bornes < 3")
            else:
                self.ErrorLabel.setText("No Indice detected")
        else:
            self.ErrorLabel.setText("No Number detected")

