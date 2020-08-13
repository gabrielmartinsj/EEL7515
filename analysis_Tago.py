from tago import Device
from tago import Analysis

def my_analysis(context, scope):

  # Acessa o dispositivo cadastrado no Tago.IO
  device_token = list(filter(lambda device_token: device_token['key'] == 'device_token',context.environment))
  device_token = device_token[0]['value']
  my_device = Device(device_token)

  # Cria dicionários para extrair os valores de umidade e temperatura
  # do bucket. Busca os últimos 24 valores, desde que tenham sido
  # coletados no último dia.
  lastValuesTemperature = {
        'variable': 'temperature',
        'start_date': '1 day',
        'qty': 24,
    }
  lastValuesHumidity = {
        'variable': 'humidity',
        'start_date': '1 day',
        'qty': 24,
    }
  lastValues_temp = my_device.find(lastValuesTemperature)
  lastValues_hum = my_device.find(lastValuesHumidity)

  # Desconsidera outras informações que são retornadas na função find(),
  # adicionando apenas os valores à lista.
  list_of_values_temp = []
  list_of_values_hum = []

  for item in lastValues_temp["result"]:
    list_of_values_temp.append(item["value"])

  for item in lastValues_hum["result"]:
    list_of_values_hum.append(item["value"])

  # Parâmetros do modelo de regressão
  B0 = -6344.226743197284
  B1 = 79.29438776
  B2 = 6.259375

  # Tira a média dos últimos valores e calcula a taxa de crescimento estimada,
  # desde que a lista não esteja vazia.
  if len(list_of_values_hum) != 0:
    average_temp = sum(list_of_values_temp)/len(list_of_values_temp)
    average_hum = sum(list_of_values_hum)/len(list_of_values_hum)
    context.log(average_hum)
    context.log(average_temp)

    predicted_growth_rate = B0 + B1*average_hum + B2*average_temp
    if average_hum < 80:
      predicted_growth_rate = 0
      context.log(predicted_growth_rate)

    # Inclui no bucket uma nova variável, Growth_Rate, com o valor estimado e a
    # unidade adequada.
    result = my_device.insert({'variable': 'Growth_Rate', 'value': predicted_growth_rate, 'unit': 'mm/h'})

  context.log('fim')
Analysis('a').init(my_analysis)
