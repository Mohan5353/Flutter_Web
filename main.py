import flet as ft

from datetime import date
from json import dump, load

from requests import get


def get_response(*args) -> dict:
    with open('Currency_Rate.json') as f:
        return load(f)


def update(*args: object) -> dict:
    present = date.today().strftime("%d %b %Y")
    response = get_response()
    file_date = response["time_last_update_utc"][5:16]
    # if present != file_date:
    #     f = open('Currency_Rate.json', 'w')
    #     url = "https://v6.exchangerate-api.com/v6/a04cc39aea88ee70a55c180c/latest/USD"
    #     response = get(url).json()
    #     dump(response, f, indent=4)
    #     f.close()
    response = response['conversion_rates']
    return response


def main(page: ft.Page) -> None:
    data = update()
    currency = sorted(data.keys())
    page.title = "Currency Converter"
    page.window_width = 400
    page.window_height = 400
    page.theme = ft.Theme(color_scheme_seed=ft.colors.ORANGE)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    from_drop = ft.Dropdown(label="From", border_width=1, options=[ft.dropdown.Option(i) for i in currency],
                            value=None, border_color=ft.colors.BLACK)
    money = ft.TextField(label="Value", border_width=1, border_color=ft.colors.BLACK, width=250,
                         prefix_icon=ft.icons.ACCOUNT_BALANCE)
    to_drop = ft.Dropdown(label="To", border_width=1, options=[ft.dropdown.Option(i) for i in currency], value=None,
                          border_color=ft.colors.BLACK)
    final = ft.Text(text_align=ft.TextAlign.CENTER, max_lines=1, size=20)

    def on_change(*args) -> None:  # noqa
        value = money.value
        if all([from_drop.value, value, to_drop.value]):
            if value.isnumeric():
                final.value = float(value) / data[from_drop.value] * data[to_drop.value]
                page.update()

    def exchange(e: ft.ControlEvent) -> None:  # noqa
        from_drop.value, to_drop.value = to_drop.value, from_drop.value
        on_change()

    def update(e: ft.ControlEvent, _data=data) -> None:  # noqa
        _data: dict = cc.update()
        on_change()

    from_drop.on_change = on_change
    money.on_change = on_change
    to_drop.on_change = on_change
    page.add(ft.Row(
        controls=[ft.Column(
            controls=[from_drop, ft.Row(
                controls=[money, ft.IconButton(icon=ft.icons.CURRENCY_EXCHANGE, on_click=exchange)]), to_drop])],
        alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Column(controls=[ft.Text()],
                       horizontal_alignment=ft.CrossAxisAlignment.CENTER))
    page.add(ft.Row(controls=[final], alignment=ft.MainAxisAlignment.CENTER))


if __name__ == '__main__':
    ft.app(main)
