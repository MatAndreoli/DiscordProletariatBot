import discord
import requests
from discord import Message, Embed

from helpers import modify_str
from shorten_url import shorten_url


async def build_fiis_msg(message: Message):
    try:
        fiis = message.content.replace('/fiis', '').strip().split(' ')
        response = requests.get(f'https://stockmarketfunction.azurewebsites.net/api/fiis?fiis={",".join(fiis)}')

        for value in response.json():
            options = { 'bold': True }
            status = 'baixa' if '-' in value.get('status') else 'alta'
            rend_distribution = value.get('rend_distribution', {})
            last_management_report = value.get('last_management_report', {})

            modified_values = {
                'code': modify_str(value.get('code'), options),
                'name': modify_str(value.get('name'), options),
                'type': modify_str(value.get('fii_type'), options),
                'current_price': modify_str(value.get('current_price', ''), options),
                'status': modify_str(value.get('status'), {
                    **options,
                    'span': { 'position': 'end', 'value': f'{status} últ. dia' }
                }),
                'average_daily': modify_str(value.get('average_daily', ''), options),
                'last_dividend': modify_str(value.get('last_dividend', ''), options),
                'dividend_yield': modify_str(value.get('dividend_yield', ''), {
                    **options,
                    'span': { 'position': 'end', 'value': 'últ. 12 meses' }
                }),
                'last_dividend_yield': modify_str(value.get('last_dividend_yield', ''), options),
                'net_worth': modify_str(value.get('net_worth', ''), options),
                'p_vp': modify_str(value.get('p_vp', ''), options),
                'last_rend_distribution': {
                    'dividend': modify_str(rend_distribution.get('dividend', ''), options),
                    'income_percentage': modify_str(rend_distribution.get('income_percentage', ''), options),
                    'pay_day': modify_str(rend_distribution.get('future_pay_day', ''), options),
                    'data_com': modify_str(rend_distribution.get('data_com', ''), options)
                },
                'last_management_report': modify_str(await shorten_url(last_management_report.get('link')), {
                    **options,
                    'span': { 'position': 'start', 'value': last_management_report.get('date', '') }
                })
            }

            result = f"Nome: {modified_values['name']}\n"
            result += f"Tipo: {modified_values['type']}\n"
            result += f"Preço atual: {modified_values['current_price']}\n"
            result += f"Status: {modified_values['status']}\n"
            result += f"Liquidez Média Diária: {modified_values['average_daily']}\n"
            result += f"Último dividendo: {modified_values['last_dividend']}\n"
            result += f"Dividend Yield: {modified_values['dividend_yield']}\n"
            result += f"Último Dividend Yield: {modified_values['last_dividend_yield']}\n"
            result += f"Patrimônio Líquido: {modified_values['net_worth']}\n"
            result += f"P/VP: {modified_values['p_vp']}\n"
            result += "Última Distribuição de Renda:\n"
            result += f"- Dividendo: {modified_values['last_rend_distribution']['dividend']}\n"
            result += f"- Rendimento: {modified_values['last_rend_distribution']['income_percentage']}\n"
            result += f"- Pagamento: {modified_values['last_rend_distribution']['pay_day']}\n"
            result += f"- Data com: {modified_values['last_rend_distribution']['data_com']}\n"
            result += f"> Último Relatório Gerencial: {modified_values['last_management_report']}\n"
            result += f"> Para mais relatórios desse FII, acesse: {await shorten_url(value.get('reports_link', ''))}\n"
            result += f"> Para mais info sobre esse FII, acesse: {await shorten_url(value.get('url', ''))}"

            embed = Embed(title=modified_values['code'], colour=discord.Colour.blue())
            embed.add_field(name='', value=result)
            await message.channel.send(embed=embed)
    except Exception as e:
        embed = Embed(title='Erro getting data', colour=discord.Colour.dark_grey())
        embed.add_field(name='', value=e)
        await message.channel.send(embed=embed)
