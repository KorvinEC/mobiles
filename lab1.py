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
            full_price_call = 0
            full_call_duration = 0
            for row in data:
                if row['msisdn_origin'] == self.number:
                    call_duration = ceil(float(row['call_duration']))
                    full_call_duration += call_duration
                    for call in call_out:
                        if not call[0]:
                            full_price_call += call_duration * call[1]
                        else:
                            full_price_call += min(call_duration, call[0]) * call[1]
                            call_duration -= call[0]
                elif row['msisdn_dest'] == self.number:
                    call_duration = ceil(float(row['call_duration']))
                    full_call_duration += call_duration
                    for call in call_in:
                        if not call[0]:
                            full_price_call += call_duration * call[1]
                        else:
                            full_price_call += min(call_duration, call[0]) * call[1]
                            call_duration -= call[0]
        return int(full_price_call), full_call_duration

    def ratify_sms(self, sms_value):
        with open(self.file_name) as csv_file:
            data = csv.DictReader(csv_file)
            full_price_sms = 0
            whole_sms_num = 0
            for row in data:
                if row['msisdn_origin'] == self.number:
                    sms_number = int(row['sms_number'])
                    whole_sms_num += sms_number
                    for sms in sms_value:
                        if not sms[0]:
                            full_price_sms += sms_number * sms[1]
                        else:
                            full_price_sms += min(sms_number, sms[0]) * sms[1]
                            sms_number -= sms[0]
        return int(sms_number), whole_sms_num

def main():

    number = '933156729'
    call_out = [[10.0, 2], [None, 0]]
    call_in = [[None, 4]]
    sms_value = [[10, 0], [None, 5]]

    ratify = Tarification('data.csv', number)
    Phone_cost, Phone_col = ratify.ratify_calls(call_out, call_in)
    SMS_cost, SMS_col = ratify.ratify_sms(sms_value)

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
    items = [{
        'item': 'Пакет звонков',
        'col': Phone_col,
        'units': 'Мин.',
        'price': Phone_cost,
    }, {
        'item': 'Пакет смс',
        'col': SMS_col,
        'units': 'Шт.',
        'price': SMS_cost
    }
    ]
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