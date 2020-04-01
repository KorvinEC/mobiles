import csv
from math import ceil
from PdfCreator import PdfCreator


class Tarification:
    def __init__(self, file_name, number):
        self.file_name = file_name
        self.number = number

    def ratify_calls(self, call_out, call_in):
        with open(self.file_name) as csv_file:
            data = csv.DictReader(csv_file)
            prices = []
            for row in data:
                call_duration = float(row['call_duration'])
                if row['msisdn_origin'] == self.number:
                    for call in call_out:
                        if not call[0]:
                            new_value = call_duration * call[1]
                            prices.append([
                                call_duration,
                                new_value,
                                call[1],
                                'Пакет входящих звонков'
                            ])
                        else:
                            time = min(call_duration, call[0])
                            new_value = time * call[1]
                            prices.append([
                                time,
                                new_value,
                                call[1],
                                'Пакет входящих звонков'
                            ])
                            call_duration -= call[0]
                elif row['msisdn_dest'] == self.number:
                    for call in call_in:
                        if not call[0]:
                            new_value = call_duration * call[1]
                            prices.append([
                                call_duration,
                                new_value,
                                call[1],
                                'Пакет исходящих звонков'
                            ])
                        else:
                            time = min(call_duration, call[0])
                            new_value = time * call[1]
                            prices.append([
                                time,
                                new_value,
                                call[1],
                                'Пакет исходящих звонков'
                            ])
                            call_duration -= call[0]
        return prices

    def ratify_sms(self, sms_value):
        with open(self.file_name) as csv_file:
            data = csv.DictReader(csv_file)
            prices = []
            for row in data:
                if row['msisdn_origin'] == self.number:
                    sms_number = float(row['sms_number'])
                    for sms in sms_value:
                        if not sms[0]:
                            new_value = sms_number * sms[1]
                            prices.append([
                                sms_number,
                                new_value,
                                sms[1],
                                'Пакет входящих смс'
                            ])
                        else:
                            sms_col = min(sms_number, sms[0])
                            new_value = sms_col * sms[1]
                            prices.append([
                                sms_col,
                                new_value,
                                sms[1],
                                'Пакет исходящих смс'
                            ])
                            sms_number -= sms[0]
        return prices

def main():

    number = '933156729'
    call_out = [[10.0, 2], [None, 0]]
    call_in = [[None, 4]]
    sms_value = [[10, 0], [None, 5]]

    ratify = Tarification('data.csv', number)
    calls_prices = ratify.ratify_calls(call_out, call_in)
    sms_prices = ratify.ratify_sms(sms_value)
    items = []
    for call in calls_prices:
        items.append({
            'item': call[3],
            'col': call[0],
            'units': 'Мин.',
            'price': call[2],
            'sum': call[1],
        })
    for sms in sms_prices:
        items.append({
            'item': sms[3],
            'col': sms[0],
            'units': 'Мин.',
            'price': sms[2],
            'sum': sms[1],
        })
    # print(items)
    whole_price = 0
    for call in calls_prices:
        print('Call time: {} mins, Call price: {} rub'.format(call[0], call[1]))
        whole_price += call[1]
    print('Whole price: {} rub\n'.format(whole_price))
    whole_price = 0
    for sms in sms_prices:
        print('Sms col: {} mins, Sms price: {} rub'.format(sms[0], sms[1]))
        whole_price += sms[1]
    print('Whole price: {} rub\n'.format(whole_price))

    pdf = PdfCreator()
    file_name = 'tax_tele.pdf'
    document_title = 'Счет на оплату'
    reciver_bank = 'АО "Стоун банк" Г. МОСКВА'
    INN = '7722737766'
    BIK = '044525700'
    tax_number = '30101810200000000700'
    tax_number_2 = '40702810900000002453'
    tax_number_3 = '86'
    reciver_user = 'ООО"Василек"'
    creator = 'ООО"ВАСИЛЕК", ИНН 7722737753, КПП 773301001, 109052, Москва ДОБРЫНИНСКАЯ ул, дом №70, корпус 2, тел.: '
    client = 'ООО ЛАГУНА, ИНН 7714037378, КПП 777550001, 119361, Москва г, ТУЛЬСКАЯ М.ул, дом № 4, строение 1'
    reason = '№ 20022016 от 12.02.2016'
    leader_name = 'Семенов Д.А.'
    accountant_name = 'Семенов Д.А.'

    pdf.build_pdf(file_name,
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
                  items)

    # number = '968247916'

    # call_out = [[None, 4]]
    # call_in = [[5.0, 0], [None, 1]]
    # sms_value = [[5.0, 0], [None, 1]]
    #
    # ratify = Tarification('data.csv', number)
    # print('Phone cost:', ratify.ratify_calls(call_out, call_in))
    # print('SMS cost:', ratify.ratify_sms(sms_value))


if __name__ == '__main__':
    main()