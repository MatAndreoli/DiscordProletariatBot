import discord
import requests
from discord import Message, Embed
from prettytable import PrettyTable

from helpers import modify_str
from shorten_url import shorten_url


def build_dividends_table(values):
    table = PrettyTable()
    columns = ['Tipo', 'Data Com', 'Pagamento', 'Valor']
    for column in columns:
        table.add_column(column, [])
    for value in values:
        row_list = []
        for vl in value.values():
            try:
                float_value = float(vl)
                row_list.append(f"R$ {float_value}")
            except:
                row_list.append(vl)
        table.add_row(row_list)
    return table


async def build_stocks_msg(message: Message):
    try:
        stocks = message.content.replace('/stocks', '').strip().split(' ')
        show_dividends = 'dividends' in message.content
        response = requests.get(f'https://stockmarketfunction.azurewebsites.net/api/stocks?stocks={",".join(stocks)}')

        for value in response.json():
            options = { 'bold': True }
            status = 'baixa' if '-' in value.get('status') else 'alta'

            last_management_report = value.get('last_management_report', {})

            if show_dividends:
                dividends_hist = f"```{build_dividends_table(value.get('dividends_history', []))}```"

            modified_values = {
                'code': modify_str(value.get('code'), options),
                'name': modify_str(value.get('name'), options),
                'operation_sector': modify_str(value.get('operation_sector'), options),
                'current_price': modify_str(value.get('current_price', ''), options),
                'status': modify_str(value.get('status'), {
                    **options,
                    'span': { 'position': 'end', 'value': f'{status} últ. 12 meses' }
                }),
                'average_daily': modify_str(value.get('average_daily', ''), options),
                'dividend_yield': modify_str(value.get('dividend_yield', ''), {
                    **options,
                    'span': { 'position': 'end', 'value': 'últ. 12 meses' }
                }),
                'net_worth': modify_str(value.get('net_worth', ''), options),
                'p_vp': modify_str(value.get('p_vp', ''), options),
                'p_l': modify_str(value.get('p_l', ''), options),
                'roe': modify_str(value.get('roe', ''), options),
                'cagr': modify_str(value.get('cagr', ''), {
                    **options,
                    'span': { 'position': 'end', 'value': 'lucros 5 anos' }
                }),
                'net_debt_ebitda': modify_str(value.get('net_debt_ebitda', ''), options),
                'total_stock_paper': modify_str(value.get('total_stock_paper', ''), options),
                'last_management_report': modify_str(await shorten_url(last_management_report.get('link', '')), {
                    **options,
                    'span': { 'position': 'start', 'value': last_management_report.get('date', '') }
                }),
                'reports_link': modify_str(await shorten_url(value.get('reports_link', '')), options),
                'url': modify_str(await shorten_url(value.get('url', '')), options)
            }

            result = f"Nome: {modified_values['name']}\n"
            result += f"Setor: {modified_values['operation_sector']}\n"
            result += f"Preço atual: {modified_values['current_price']}\n"
            result += f"Status: {modified_values['status']}\n"
            result += f"Liquidez Média Diária: {modified_values['average_daily']}\n"
            result += f"Dividend Yield: {modified_values['dividend_yield']}\n"
            result += f"Patrimônio Líquido: {modified_values['net_worth']}\n"
            result += f"P/VP: {modified_values['p_vp']}\n"
            result += f"P/L: {modified_values['p_l']}\n"
            result += f"ROE: {modified_values['roe']}\n"
            result += f"CAGR: {modified_values['cagr']}\n"
            result += f"Dívida Líquida/EBITDA: {modified_values['net_debt_ebitda']}\n"
            result += f"Total de papéis: {modified_values['total_stock_paper']}\n"
            result += f"Último Relatório Trimestral: {modified_values['last_management_report']}\n"

            result += f"> Para mais relatórios desse FII, acesse: {modified_values['reports_link']}\n"
            result += f"> Para mais info sobre esse FII, acesse: {modified_values['url']}"

            embed = Embed(title=value.get('code'), colour=discord.Colour.dark_red())
            embed.add_field(name='', value=result)
            await message.channel.send(embed=embed)
            if show_dividends:
                dividends_embed = Embed(title=f"{value.get('code')}: Dividends", colour=discord.Colour.dark_red())
                dividends_embed.add_field(name='', value=dividends_hist)
                await message.channel.send(embed=dividends_embed)
    except Exception as e:
        embed = Embed(title='Erro getting data', colour=discord.Colour.dark_grey())
        embed.add_field(name='', value=e)
        await message.channel.send(embed=embed)
