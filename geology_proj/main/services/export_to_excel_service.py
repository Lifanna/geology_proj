import openpyxl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.alignment import Alignment
from openpyxl.styles import Font
from main import models
from openpyxl.utils import get_column_letter
import json


class ExportToExcelService:
    def __init__(self):
        self.workbook = openpyxl.load_workbook("main/services/example.xlsx")
        self.worksheet_1 = self.workbook.active
        self.worksheet_2 = self.workbook.get_sheet_by_name('Стр. 2')
        # self.worksheet_2 = self.workbook.active

    # def build_document(self, license : models.License, 
    #                    watercourse: models.WaterCourse, 
    #                    watercourse_bound: models.LicenseWaterCourse, 
    #                    line: models.Line, 
    #                    wells
    # ):
    #     error_message = ""
    #     filepath = "main/services/asd.xlsx"
    #     well_depths = {}
    #     with open('main/services/wellDepths.json', mode="r", encoding='utf8') as wellDepths:
    #         well_depths = json.load(wellDepths)

    #     try:
    #         self.worksheet.title = license.short_name

    #         self.worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=17)
    #         self.worksheet.cell(column=1, row=1, value=license.short_name)
    #         self.worksheet.cell(column=1, row=1).font = Font(bold=True)

    #         row_index = 2
    #         for well in wells:
    #             self.worksheet.merge_cells(start_row=row_index, start_column=1, end_row=row_index, end_column=13)
    #             self.worksheet.cell(column=1, row=row_index, value="Описание разреза отложений по скважине")

    #             row_index += 1

    #             # отображаем водотоки
    #             self.worksheet.merge_cells(start_row=row_index, start_column=1, end_row=row_index, end_column=5)
    #             self.worksheet.cell(column=1, row=row_index, value=watercourse.name)

    #             # если имеется главный водоток
    #             if watercourse_bound.parent_watercourse and watercourse_bound.parent_watercourse.id != watercourse_bound.watercourse.id:
    #                 self.worksheet.cell(column=6, row=row_index, value=watercourse_bound.parent_watercourse.name)

    #             row_index += 1

    #             # отображаем линии
    #             self.worksheet.cell(column=1, row=row_index, value=line.name)

    #             row_index += 1

    #             # отображаем сведения о скважинах и их интервалах
    #             self.worksheet.cell(column=14, row=row_index, value=well.name)
    #             row_index += 1
    #             # отображаем даты бурения скважин: начала и окончания
    #             self.worksheet.cell(column=1, row=row_index, value="Бурение начато")
    #             self.worksheet.cell(column=1, row=row_index, value=well.created_at.date())
    #             self.worksheet.cell(column=6, row=row_index, value="Бурение окончено")
    #             self.worksheet.cell(column=6, row=row_index, value=well.updated_at.date()) 
    #             row_index += 1

    #             layers = models.Layer.objects.filter(well__id=well.id)

    #             self.worksheet.merge_cells(start_row=row_index, start_column=1, end_row=row_index + 2, end_column=1)
    #             self.worksheet.cell(column=1, row=row_index, value="№ проходки/пробы")

    #             self.worksheet.merge_cells(start_row=row_index, start_column=2, end_row=row_index, end_column=3)
    #             self.worksheet.cell(column=2, row=row_index, value="Глубина, м")
    #             self.worksheet.merge_cells(start_row=row_index + 1, start_column=2, end_row=row_index + 2, end_column=2)
    #             self.worksheet.cell(column=2, row=row_index + 1, value="скв-ны")
    #             self.worksheet.merge_cells(start_row=row_index + 1, start_column=3, end_row=row_index + 2, end_column=3)
    #             self.worksheet.cell(column=3, row=row_index + 1, value="обсада")

    #             self.worksheet.cell(column=4, row=row_index, value="Диаметр бурения, мм")
    #             self.worksheet.cell(column=5, row=row_index, value="Литологическая колонка")
    #             self.worksheet.cell(column=6, row=row_index, value="Глубина контакта")
    #             self.worksheet.cell(column=7, row=row_index, value="Мощность")
    #             self.worksheet.cell(column=8, row=row_index, value="Кат. пород")
    #             self.worksheet.cell(column=9, row=row_index, value="Отметка о водоносности")
    #             self.worksheet.cell(column=10, row=row_index, value="Выход керна")

    #             self.worksheet.merge_cells(start_row=row_index, start_column=11, end_row=row_index, end_column=12)
    #             self.worksheet.merge_cells(start_row=row_index, start_column=11, end_row=row_index + 1, end_column=11)
    #             self.worksheet.merge_cells(start_row=row_index, start_column=12, end_row=row_index + 1, end_column=12)
    #             self.worksheet.cell(column=11, row=row_index, value="Выход керна")

    #             row_index += 3

    #             depths_row_index = row_index
    #             for number, depth_value in well_depths.get("wellDepths").items():
    #                 self.worksheet.cell(column=1, row=depths_row_index, value=str(number))
    #                 self.worksheet.cell(column=2, row=depths_row_index, value=str(depth_value))
    #                 self.worksheet.merge_cells(start_row=depths_row_index, start_column=1, end_row=depths_row_index + 5, end_column=1)

    #                 depths_row_index += 6

    #             self.worksheet.merge_cells(start_row=row_index, start_column=6, end_row=row_index + 50, end_column=6)
    #             self.worksheet.merge_cells(start_row=row_index, start_column=6, end_row=row_index + 59, end_column=6)
    #             self.worksheet.merge_cells(start_row=row_index, start_column=6, end_row=row_index + 78, end_column=6)

    #             self.worksheet.merge_cells(start_row=row_index, start_column=7, end_row=row_index + 50, end_column=7)
    #             self.worksheet.merge_cells(start_row=row_index, start_column=7, end_row=row_index + 59, end_column=7)
    #             self.worksheet.merge_cells(start_row=row_index, start_column=7, end_row=row_index + 78, end_column=7)

    #             for layer in layers:
    #                 # self.worksheet.cell(column=6, row=row_index, value=layer.name)

    #                 # диаметр бурения, мм
    #                 self.worksheet.cell(column=4, row=row_index, value="151")

    #                 row_index += 1

    #             row_index += 1

    #         self.workbook.save(filepath)
    #         self.workbook.close()
    #     except Exception as e:
    #         print("ERROR: ", e)
    #         error_message = e
    #     finally:
    #         return error_message

    def build_document(self, license : models.License, 
                       watercourse: models.WaterCourse, 
                       watercourse_bound: models.LicenseWaterCourse, 
                       line: models.Line, 
                       well
    ):
            error_message = ""
            filepath = "media/example.xlsx"
        # try:
            self.worksheet_1.title = license.short_name

            self.worksheet_1.cell(column=1, row=1, value=license.short_name)
            self.worksheet_1.cell(column=1, row=1).font = Font(bold=True)

            self.worksheet_1.cell(column=14, row=2, value=well.name)

            # отображаем водотоки
            self.worksheet_1.cell(column=1, row=3, value=watercourse.name)

            # если имеется главный водоток
            if watercourse_bound.parent_watercourse and watercourse_bound.parent_watercourse.id != watercourse_bound.watercourse.id:
                self.worksheet_1.cell(column=6, row=3, value=watercourse_bound.parent_watercourse.name)

            # отображаем линии
            self.worksheet_1.cell(column=1, row=4, value=line.name)
            self.worksheet_1.cell(column=6, row=4, value=well.name)

            # отображаем сведения о скважинах и их интервалах
            # отображаем даты бурения скважин: начала и окончания
            self.worksheet_1.cell(column=3, row=5, value=well.created_at.date())
            self.worksheet_1.cell(column=12, row=5, value=well.updated_at.date())

            layers = models.Layer.objects.filter(well__id=well.id)

            row_index = 9
            prev_depth = 0

            # отображаем сведения о слоях
            for layer in layers:
                thin_border = Border(left=Side(style='thin'), 
                                    right=Side(style='thin'), 
                                    top=Side(style='thin'), 
                                    bottom=Side(style='thin'))
                layer_capacity = layer.depth - prev_depth

                if layer.aquifer == True:
                    aquifer = "Да"
                else:
                    aquifer = "Нет"
                # глубина
                if layer.depth - prev_depth > 0.5:
                    end_row_index = int((layer.depth - prev_depth) / 0.5) * 5 - 1
                    self.worksheet_1.cell(column=6, row=row_index, value=layer.depth)
                    self.worksheet_1.cell(column=7, row=row_index, value=str(layer_capacity))
                    self.worksheet_1.cell(column=9, row=row_index, value=aquifer)
                    self.worksheet_1.cell(column=6, row=row_index).border = thin_border
                    self.worksheet_1.cell(column=6, row=row_index).alignment = Alignment(horizontal='center', vertical='center')
                    self.worksheet_1.merge_cells(
                        start_row=row_index, start_column=6, end_row=row_index + end_row_index, end_column=6)
                    self.worksheet_1.cell(column=7, row=row_index).border = thin_border
                    self.worksheet_1.cell(column=7, row=row_index).alignment = Alignment(horizontal='center', vertical='center')
                    self.worksheet_1.merge_cells(
                        start_row=row_index, start_column=7, end_row=row_index + end_row_index, end_column=7)
                    self.worksheet_1.cell(column=9, row=row_index).border = thin_border
                    self.worksheet_1.cell(column=9, row=row_index).alignment = Alignment(horizontal='center', vertical='center')
                    self.worksheet_1.merge_cells(
                        start_row=row_index, start_column=9, end_row=row_index + end_row_index, end_column=9)
                    row_index += end_row_index + 1
                elif layer.depth - prev_depth == 0.5:
                    self.worksheet_1.cell(column=6, row=row_index, value=layer.depth)
                    self.worksheet_1.cell(column=7, row=row_index, value=str(layer_capacity))
                    self.worksheet_1.cell(column=6, row=row_index).border = thin_border
                    self.worksheet_1.cell(column=6, row=row_index).alignment = Alignment(horizontal='center', vertical='center')
                    self.worksheet_1.merge_cells(
                        start_row=row_index, start_column=6, end_row=row_index + 4, end_column=6)
                    self.worksheet_1.cell(column=7, row=row_index).border = thin_border
                    self.worksheet_1.cell(column=7, row=row_index).alignment = Alignment(horizontal='center', vertical='center')
                    self.worksheet_1.merge_cells(
                        start_row=row_index, start_column=7, end_row=row_index + 4, end_column=7)

                    row_index += 5

                prev_depth = layer.depth

            row_index = 4
            prev_depth = 0
            self.worksheet_2.cell(column=2, row=1, value=well.name)
            for layer in layers:
                thin_border = Border(left=Side(style='thin'), 
                                    right=Side(style='thin'), 
                                    top=Side(style='thin'), 
                                    bottom=Side(style='thin'))
                self.worksheet_2.cell(column=1, row=row_index, value=prev_depth)
                self.worksheet_2.cell(column=2, row=row_index, value=layer.depth)

                self.worksheet_2.merge_cells(
                        start_row=row_index, start_column=1, end_row=row_index + 4, end_column=1)
                
                self.worksheet_2.merge_cells(
                        start_row=row_index, start_column=2, end_row=row_index + 4, end_column=2)

                self.worksheet_2.cell(column=3, row=row_index, value=layer.layer_material.name)
                self.worksheet_2.merge_cells(
                        start_row=row_index, start_column=3, end_row=row_index + 4, end_column=10)

                prev_depth = layer.depth
                row_index += 5

            self.workbook.save(filepath)
            self.workbook.close()
        # except Exception as e:
        #     print("ERROR: ", e)
        #     error_message = e
        # finally:
        #     return error_message
