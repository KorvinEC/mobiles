from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from num2words import num2words
import datetime
import locale


def create_items(items):
    result_summ = 0
    result_list = []
    result_list.append(
        ['№', 'Товары (работы, услуги)', 'Кол-во', 'Ед.', "Цена", "Сумма"]
    )
    for item, i in zip(items, range(len(items))):
        result_summ += item['sum']
        result_summ = round(result_summ, 2)
        result_list.append(
            [i + 1, str_format(item['item'], 50), item['col'], item['units'], item['price'], item['sum']]
        )
    return result_list, result_summ, len(result_list) - 1


def str_format(input_str, range_len):
    if len(input_str) >= range_len:
        space_addr = input_str[range_len::-1].find(' ')
        input_str = input_str[:range_len - space_addr] + '\n' + str_format(input_str[range_len - space_addr:], range_len)
    else:
        pass
    return input_str


class PdfCreator:
    def build_pdf(self,
                  file_name,
                  document_title,
                  reciver_bank,
                  INN,
                  BIK,
                  tax_number,
                  tax_number_2,
                  tax_number_3,
                  reciver_user,
                  creator,
                  client,
                  reason,
                  leader_name,
                  accountant_name,
                  items
                  ):

        pdfmetrics.registerFont(
            TTFont('Arial', 'Arial.ttf')
        )
        pdfmetrics.registerFont(
            TTFont('Arial_Bold', 'ArialBold.ttf')
        )
        pdf = SimpleDocTemplate(file_name,
                                pagesize=A4,
                                rightMargin=72.5,
                                leftMargin=25,
                                topMargin=32.5,
                                bottomMargin=80,
                                title=document_title
                                )

        ''''''''''''''''''''''''''''''''''''''''''''''''''
        table_0 = Table([
            [reciver_bank],
            ['Банк получателя']
        ], 250)
        table_0_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            # ('SIZE', (0, 0), (0, 0), 10),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
        table_0.setStyle(table_0_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        table_1 = Table([
            ['БИК'],
            ['Сч. №']
        ], 50)
        table_1_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (0, 0), 0.5, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
        table_1.setStyle(table_1_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        table_2 = Table([
            [BIK],
            [tax_number]
        ], 200)
        table_2_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
        table_2.setStyle(table_2_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        table_30 = Table([
            ['Инн ' + INN, 'КПП ' + '772201001']
        ], [125, 125])
        table_30_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black),
            ('LINEAFTER', (0, 0), (0, 0), 0.5, colors.black)
        ])
        table_30.setStyle(table_30_style)

        table_3 = Table([
            [table_30],
            [reciver_user],
            ['Получатель']
        ], 250)
        table_3_style = TableStyle([
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ])
        table_3.setStyle(table_3_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        table_4 = Table([
            ['Сч. №']
        ], 50)
        table_4_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('VALiGN', (0, 0), (0, 0), 'TOP'),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
        table_4.setStyle(table_4_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        table_5 = Table([
            [tax_number_2]
        ], 200)
        table_5_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ])
        table_5.setStyle(table_5_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        table_table_0 = Table([
            [table_0, table_1, table_2],
            [table_3, table_4, table_5]
        ], [250, 50, 200])
        table_table_0_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALiGN', (0, 1), (0, 1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
        table_table_0.setStyle(table_table_0_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        locale.setlocale(locale.LC_ALL, 'ru.UTF-8')
        date_number = datetime.datetime.today().strftime('%d %b %y')
        table_date = Table([
            ['Счет на оплату № ' + tax_number_3 + ' от ' + str(date_number)]
        ], 500)
        table_date_style = TableStyle([
            # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('LINEBELOW', (0, 0), (0, 0), 2, colors.black),
            ('FONTNAME', (0, 0), (0, 0), 'Arial_Bold'),
            ('BOTTOMPADDING', (0, 0), (0, 0), 15),
            ('TOPPADDING', (0, 0), (0, 0), 15),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('SIZE', (0, 0), (0, 0), 14),
        ])
        table_date.setStyle(table_date_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        table_data = Table([
            ['Поставщик\n(Исполнитель):', str_format(input_str=creator, range_len=75)],
            ['Покупатель\n(Заказчик):', str_format(input_str=client, range_len=75)],
            ['Основание:', reason]
        ])
        table_data_style = TableStyle([
            ('FONTNAME', (0, 0), (0, 2), 'Arial'),
            ('FONTNAME', (1, 0), (1, 2), 'Arial_Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (1, 0), (1, 2), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
        table_data.setStyle(table_data_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        items, final_sum, result_col = create_items(items)
        table_table_1 = Table(
            items,
            [20, 270, 50, 35, 62.5, 62.5]
        )
        table_table_1_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
            ('FONTNAME', (0, 0), (-1, 0), 'Arial_Bold'),
            ('AlIGN', (0, 0), (5, 0), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ])
        table_table_1.setStyle(table_table_1_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        table_result = Table([
            ['Итого', '{:.2f}'.format(final_sum)],
            ['В том числе НДС', round(final_sum - (final_sum / 1.2), 2)],
            ['Всего к оплате', '{:.2f}'.format(final_sum)]
        ], [430, 70])
        table_result_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('FONTNAME', (0, 0), (-1, -1), 'Arial_Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ])
        table_result.setStyle(table_result_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        number_str = num2words('{:.2f}'.format(final_sum), lang='ru').format().split('запятая')
        table_overall = Table([
            ['Всего наименований {} на сумму {:.2f} руб.'.format(result_col, final_sum)],
            ['{} рублей {} копеек'.format(number_str[0], number_str[1])]
        ], 500)
        table_overall_style = TableStyle([
            ('FONTNAME', (0, 0), (0, 0), 'Arial'),
            ('FONTNAME', (0, 1), (0, 1), 'Arial_Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
        table_overall.setStyle(table_overall_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        text = 'Внимание!\n' \
               'Оплата данного счета означает согласие с условиями поставки товара.\n' \
               'Уведомление об оплате обязательно, в противном случае не гарантируется наличие товара на складе.\n' \
               'Товар отпускается по факту прихода денег на р/с Поставщика, самовывозом, при наличии доверенности\nи паспорта.'

        table_attention = Table([
            [text]
        ], 500)
        table_attention_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('SIZE', (0, 0), (-1, -1), 9),
            ('LINEBELOW', (0, 0), (0, 0), 2, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
        table_attention.setStyle(table_attention_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        table_sign = Table([
            ['Руководитель', leader_name, 'Бухгалтер', accountant_name]
        ], [75, 175, 75, 175])
        table_sign_style = TableStyle([
            # ('GRID', (0,0), (-1,-1), 2, colors.black),
            ('LINEBELOW', (1, 0), (1, 0), 2, colors.black),
            ('SIZE', (1, 0), (1, 0), 6),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('LINEBELOW', (3, 0), (3, 0), 2, colors.black),
            ('SIZE', (3, 0), (3, 0), 6),
            ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('SIZE', (0, 0), (0, 0), 9),
            ('SIZE', (-2, 0), (-2, 0), 9),
        ])
        table_sign.setStyle(table_sign_style)
        ''''''''''''''''''''''''''''''''''''''''''''''''''
        result_table = Table([
            [table_table_0],
            [table_date],
            [table_data],
            [table_table_1],
            [table_result],
            [table_overall],
            [table_attention],
            [table_sign]
        ])

        result_table_style = TableStyle([
            # ('GRID', (0,0), (-1,-1), 2, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 4), (0, 7), 5),
            ('BOTTOMPADDING', (0, 4), (0, 7), 5),
        ])
        result_table.setStyle(result_table_style)
        elems = []
        elems.append(result_table)
        pdf.build(elems)
