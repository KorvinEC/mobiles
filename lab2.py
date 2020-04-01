import csv
import matplotlib.pyplot as plt
from matplotlib.dates import datestr2num
import matplotlib.dates as mdates
from math import ceil
from PdfCreator import PdfCreator


def convert_bytes(input_bytes, from_b, to_b, bsize=1024):
    degrees = {'b': 0, 'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
    result = float(input_bytes)
    if degrees[from_b] > degrees[to_b]:
        for i in range(degrees[from_b]):
            result = result * bsize
        return result
    elif degrees[from_b] < degrees[to_b]:
        for i in range(degrees[to_b]):
            result = result / bsize
        return result
    else:
        return result


def cleaner():
    with open('dump.txt', 'r') as file:
        lines = []
        for line in file:
            lines.append(line.split(' '))
    clean_data = [[]]
    lines[0] = [s for s in lines[0] if s != '']
    clean_data[0] = [
        lines[0][0] + ' ' + lines[0][1] + ' ' + lines[0][2],
        lines[0][3],
        lines[0][4],
        lines[0][5],
        lines[0][6] + ' ' + lines[0][7] + ' ' + lines[0][8],
        lines[0][9] + ' ' + lines[0][10] + ' ' + lines[0][11],
        lines[0][12] + ' ' + lines[0][13] + ' ' + lines[0][14],
        lines[0][15] + ' ' + lines[0][16] + ' ' + lines[0][17],
        lines[0][18] + ' ' + lines[0][19],
        lines[0][20] + ' ' + lines[0][21][:-1]
    ]
    for i in range(1, len(lines[1:-4])):
        lines[i] = [s for s in lines[i] if s != '' and s != '->']
        clean_data += [[
            lines[i][0] + ' ' + lines[i][1].split(".")[0],
            lines[i][2],
            lines[i][3],
            lines[i][4],
            lines[i][5],
            lines[i][6],
            lines[i][7],
            lines[i][8],
            lines[i][9],
            lines[i][10][:-1],
        ]]
    with open('clean_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(clean_data)


class TarificationNet:
    def __init__(self, file_name, ip):
        self.file_name = file_name
        self.ip = ip

    def ratify_ip(self, prices):
        with open(self.file_name) as csv_file:
            data = csv.DictReader(csv_file)
            full_bytes = 0.
            for row in data:
                if self.ip in row['Src IP Addr:Port'] or self.ip in row['Dst IP Addr:Port']:
                    full_bytes += ceil(float(row['In Byte']))
        full_price = []
        for price in prices:
            if price[0] == 'length':
                if not price[1]:
                    new_bytes = convert_bytes(full_bytes, 'b', price[3])
                    value = round(price[2] * new_bytes, 2)
                    full_price.append([
                        'Интернет',
                        round(new_bytes, 2),
                        price[3] + 'b',
                        price[2],
                        value,
                    ])
                else:
                    bytes_value = min(convert_bytes(full_bytes, 'b', price[3]), convert_bytes(price[1], 'b', price[3]))
                    full_price += price[2] * bytes_value
                    full_bytes -= price[1]
            if price[0] == 'ladder':
                new_price = price[2]
                bytes_buff = full_bytes
                while bytes_buff >= 0:
                    bytes_value = min(convert_bytes(bytes_buff, 'b', price[3]), convert_bytes(price[1], 'b', price[3]))
                    full_price += new_price * bytes_value
                    bytes_buff -= price[1]
                    new_price += price[2]
        return full_price
        # return full_bytes, full_price

    def graph_stat(self):
        with open(self.file_name) as csv_file:
            data = csv.DictReader(csv_file)
            out_data_dict = {}
            in_data_dict = {}
            for row in data:
                if self.ip in row['Src IP Addr:Port']:
                    out_data_dict.update({
                        datestr2num(row['Date first seen']): ceil(float(row['In Byte']))
                    })
                elif self.ip in row['Dst IP Addr:Port']:
                    in_data_dict.update({
                        datestr2num(row['Date first seen']): ceil(float(row['In Byte']))
                    })

        sorted_out_data_dict = {}
        sorted_in_data_dict = {}

        for i, z in zip(sorted(out_data_dict), sorted(in_data_dict)):
            sorted_out_data_dict.update({
                i: out_data_dict[i]
            })
            sorted_in_data_dict.update({
                z: in_data_dict[z]
            })

        fig, ax = plt.subplots()
        ax.plot(list(sorted_out_data_dict.keys()), list(sorted_out_data_dict.values()),'-', label='Out data')
        ax.plot(list(sorted_in_data_dict.keys()), list(sorted_in_data_dict.values()),'-', label='Inc data')
        ax.xaxis.set_major_locator(mdates.HourLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_minor_locator(mdates.MinuteLocator())
        ax.legend()
        plt.show()

def main():
    file = 'clean_data.csv'
    target_ip = '77.74.181.52'
    prices = [
        ['length',   # type of charge
         None,       # charge package
         1.5,        # charge
         'k']        # charge dimension    1.5 per kilobyte
    ]

    ratify = TarificationNet(file, target_ip)
    net_prices = ratify.ratify_ip(prices)
    for price in net_prices:
        print('Bytes: {} {}\nPrice: {} rub'.format(price[1], price[2], price[4]))

    # items = []
    # for price in net_prices:
    #     items.append({
    #         'item': price[0],
    #         'col': price[1],
    #         'units': price[2],
    #         'price': price[3],
    #         'sum': price[4],
    #     })
    # print(items)
    #
    # pdf = PdfCreator()
    # file_name = 'tax_inet.pdf'
    # document_title = 'Счет на оплату'
    # reciver_bank = 'АО "Стоун банк" Г. МОСКВА'
    # INN = '7722737766'
    # BIK = '044525700'
    # tax_number = '30101810200000000700'
    # tax_number_2 = '40702810900000002453'
    # tax_number_3 = '86'
    # reciver_user = 'ООО"Василек"'
    # date_number = '01 июля 2016 г.'
    # creator = 'ООО"ВАСИЛЕК", ИНН 7722737753, КПП 773301001, 109052, Москва ДОБРЫНИНСКАЯ ул, дом №70, корпус 2, тел.: '
    # client = 'ООО ЛАГУНА, ИНН 7714037378, КПП 777550001, 119361, Москва г, ТУЛЬСКАЯ М.ул, дом № 4, строение 1'
    # reason = '№ 20022016 от 12.02.2016'
    # leader_name = 'Семенов Д.А.'
    # accountant_name = 'Семенов Д.А.'
    # pdf.build_pdf(file_name,
    #               document_title,
    #               reciver_bank,
    #               INN,
    #               BIK,
    #               tax_number,
    #               tax_number_2,
    #               tax_number_3,
    #               reciver_user,
    #               creator,
    #               client,
    #               reason,
    #               leader_name,
    #               accountant_name,
    #               items)


    # ratify.graph_stat()

    # target_ip = '192.168.250.1'
    # prices = [
    #     ['ladder',
    #      convert_bytes(500, 'k', 'b'),
    #      0.5,
    #      'k']
    # ]
    # ratify = TarificationNet(file, target_ip)
    # ratify.ratify_ip(prices)
    # # ratify.graph_stat()


if __name__ == '__main__':
    main()