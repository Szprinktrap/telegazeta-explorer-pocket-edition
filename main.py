import math
import re
import sys
import requests
from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox

historia = ['100|1']
kanal = 1
selected_radiobutton = 1

link_do_obrazka = "http://telegazeta.tvp.pl/sync/ncexp/TG1/100/100_0001.png"
mozna_dalej = True
podstrona = 0
pobrana_strona = 0

pageinput_val = "100"

screen = AsyncImage(source=link_do_obrazka, allow_stretch=True).__self__
subpagecounter = Label(text="1").__self__
subpageprev = Button(text="<<").__self__
subpagenext = Button(text=">>").__self__
channelname = Label(text="Telegazeta TVP 1").__self__
pageinput = TextInput(text='100').__self__

error_popup_layout = GridLayout(cols=1, row_force_default=True, row_default_height=100).__self__
error_label = Label(text="Placeholder").__self__
error_dismiss = Button(text="Zamknij").__self__
error_dismiss.on_press = lambda: error_popup.dismiss()
error_popup_layout.add_widget(error_label)
error_popup_layout.add_widget(error_dismiss)
error_popup = Popup(title='Wystąpił błąd! :(', content=error_popup_layout, size_hint=(None, None), size=(600, 500))

current_tvp_channel = "TG1"
current_polsat_channel = "gazetatvpolsat"

subpageprev.disabled = True


def tvp_fetch(page, subpage, channel, append):
    try:
        global link_do_obrazka
        global mozna_dalej
        global podstrona
        global pobrana_strona
        global error_label
        global error_popup
        subpage_digitnum = int(math.log10(subpage)) + 1
        if subpage_digitnum == 1:
            subpage_str = "000" + str(subpage)
        elif subpage_digitnum == 2:
            subpage_str = "00" + str(subpage)
        elif subpage_digitnum == 3:
            subpage_str = "0" + str(subpage)
        elif subpage_digitnum == 4:
            subpage_str = str(subpage)
        r = requests.get(
            "http://www.telegazeta.pl/telegazeta.php?channel=" + channel + "&page=" + str(page) + "_" + subpage_str)
        image = r.text.split('<div id="ekran"><img src="')[1].split('"')[0]
        curr_subpage = r.text.split('podstrona ')[1].split(' z')[0]
        max_subpages = r.text.split('podstrona ' + str(subpage) + " z ")[1].split('"')[0]
        curr_page = r.text.split('strona ')[1].split(",")[0]
        print("status: " + str(r.status_code))
        print("url obrazu: " + image)
        print("ilość podstron: " + max_subpages)
        print("aktualna podstrona: " + curr_subpage)
        print("aktualna strona: " + curr_page)
        link_do_obrazka = image
        pobrana_strona = int(curr_page)
        podstrona = int(curr_subpage)
        if curr_subpage == max_subpages:
            mozna_dalej = False
        else:
            mozna_dalej = True
        print("można na następną podstronę: " + str(mozna_dalej))
        if append:
            historia.append(curr_page + "|" + curr_subpage)
    except:
        err = sys.exc_info()[0]
        error_label.text = err
        error_popup.open()


def polsat_fetch(page, subpage, channel, append):
    try:
        global link_do_obrazka
        global mozna_dalej
        global podstrona
        global pobrana_strona
        global error_label
        global error_popup
        subpage_digitnum = int(math.log10(subpage)) + 1
        if subpage_digitnum == 1:
            subpage_str = "000" + str(subpage)
        elif subpage_digitnum == 2:
            subpage_str = "00" + str(subpage)
        elif subpage_digitnum == 3:
            subpage_str = "0" + str(subpage)
        elif subpage_digitnum == 4:
            subpage_str = str(subpage)
        r = requests.get("http://" + channel + ".pl/" + str(page) + "/" + subpage_str)
        image = "http://" + channel + ".pl/" + r.text.split('<center><img width="90%" src="')[1].split('"')[0]
        curr_subpage = re.split("<title>Gazeta .*? strona:", r.text)[1].split('/')[1].split('<')[0]
        curr_page = re.split("<title>Gazeta .*? strona:", r.text)[1].split("/")[0]
        if "png" in image:
            print("status: " + str(r.status_code))
            print("url obrazu: " + image)
            print("ilość podstron: nie sprawdzane w przypadku polsatu")
            print("aktualna podstrona: " + curr_subpage)
            print("aktualna strona: " + curr_page)
            link_do_obrazka = image
            pobrana_strona = int(curr_page)
            podstrona = int(curr_subpage)
            if 'class="btn btn-default"><span class="glyphicon glyphicon-arrow-right"></span></a></div>        </div>' in r.text:
                mozna_dalej = True
            else:
                mozna_dalej = False

                print("można na następną podstronę: " + str(mozna_dalej))
            if append:
                historia.append(curr_page + "|" + curr_subpage)

        else:
            link_do_obrazka = "http://" + channel + ".pl/" + "//teletext/100/100_0001.png"
            pobrana_strona = 100
            podstrona = 1
            mozna_dalej = True
            print("status: " + str(r.status_code))
            print("url obrazu: " + image)
            print("ilość podstron: nie sprawdzane w przypadku polsatu")
            print("aktualna podstrona: " + curr_subpage)
            print("aktualna strona: " + curr_page)
            print("można na następną podstronę: " + str(mozna_dalej))
            if append:
                historia.append("100|1")

    except:
        err = sys.exc_info()[0]
        error_label.text = err
        error_popup.open()


def on_text(instance, value):
    global pageinput_val
    print('The widget', instance, 'have:', value)
    pageinput_val = value


def on_checkbox_active(checkbox, value):
    global selected_radiobutton
    if value:
        print('Checkbox', checkbox, 'is active')
        selected_radiobutton = checkbox


def navigate_callback(page, subpage, append):
    print("wciśnięto")
    global pageinput_val
    global screen
    global link_do_obrazka
    global subpageprev
    global subpagenext
    global subpagecounter
    global mozna_dalej
    global podstrona
    global kanal
    global current_tvp_channel
    global current_polsat_channel

    if kanal == 1:
        tvp_fetch(page, subpage, current_tvp_channel, append)
    elif kanal == 2:
        polsat_fetch(page, subpage, current_polsat_channel, append)

    screen.source = link_do_obrazka
    screen.reload()
    subpagecounter.text = str(podstrona)
    pageinput.text = str(pobrana_strona)

    if mozna_dalej:
        subpagenext.disabled = False
    else:
        subpagenext.disabled = True

    if podstrona == 1:
        subpageprev.disabled = True
    else:
        subpageprev.disabled = False


def chchannel(chooser):
    global selected_radiobutton
    global kanal
    global current_tvp_channel
    global current_polsat_channel
    global historia
    global channelname

    if selected_radiobutton == 1:
        kanal = 1
        current_tvp_channel = "TG1"
        channelname.text = "Telegazeta TVP 1"
    elif selected_radiobutton == 2:
        kanal = 1
        current_tvp_channel = "TG2"
        channelname.text = "Telegazeta TVP 2"
    elif selected_radiobutton == 3:
        kanal = 1
        current_tvp_channel = "SAT"
        channelname.text = "Telegazeta TVP Polonia"
    elif selected_radiobutton == 4:
        kanal = 1
        current_tvp_channel = "KUL"
        channelname.text = "Telegazeta TVP Kultura"
    elif selected_radiobutton == 5:
        kanal = 1
        current_tvp_channel = "SPO"
        channelname.text = "Telegazeta TVP Sport"
    elif selected_radiobutton == 6:
        kanal = 2
        current_polsat_channel = "gazetatvpolsat"
        channelname.text = "Gazeta TV Polsat"
    elif selected_radiobutton == 7:
        kanal = 2
        current_polsat_channel = "gazetatv4"
        channelname.text = "Gazeta TV4"

    historia.clear()
    navigate_callback(100, 1, True)
    chooser.dismiss()


def prev_page():
    print(historia)
    print(len(historia))
    if len(historia) == 1:
        error_label.text = "Nie mam się gdzie cofać!"
        error_popup.open()
    else:
        prevpage = historia[len(historia) - 2]
        prevpage_data = prevpage.split("|")
        navigate_callback(int(prevpage_data[0]), int(prevpage_data[1]), False)
        historia.remove(historia[len(historia) - 1])


class TelegazetaExplorerApp(App):
    def build(self):
        global screen
        global subpagecounter
        global subpageprev
        global subpagenext
        global channelname
        global pageinput
        global pageinput_val
        global podstrona
        global pobrana_strona
        global error_popup
        global error_label

        ch_chooser_layout = GridLayout(cols=2, row_force_default=True, row_default_height=120).__self__
        cb_tvp1 = CheckBox(group="ch").__self__
        cb_tvp1.on_press = lambda: on_checkbox_active(1, cb_tvp1.active)
        lb_tvp1 = Label(text="TVP1").__self__
        cb_tvp2 = CheckBox(group="ch").__self__
        cb_tvp2.on_press = lambda: on_checkbox_active(2, cb_tvp2.active)
        lb_tvp2 = Label(text="TVP2").__self__
        cb_tvppol = CheckBox(group="ch").__self__
        cb_tvppol.on_press = lambda: on_checkbox_active(3, cb_tvppol.active)
        lb_tvppol = Label(text="TVP Polonia").__self__
        cb_tvpkul = CheckBox(group="ch").__self__
        cb_tvpkul.on_press = lambda: on_checkbox_active(4, cb_tvpkul.active)
        lb_tvpkul = Label(text="TVP Kultura").__self__
        cb_tvpspo = CheckBox(group="ch").__self__
        cb_tvpspo.on_press = lambda: on_checkbox_active(5, cb_tvpspo.active)
        lb_tvpspo = Label(text="TVP Sport").__self__
        cb_polsat = CheckBox(group="ch").__self__
        cb_polsat.on_press = lambda: on_checkbox_active(6, cb_polsat.active)
        lb_polsat = Label(text="Polsat").__self__
        cb_tv4 = CheckBox(group="ch").__self__
        cb_tv4.on_press = lambda: on_checkbox_active(7, cb_tv4.active)
        lb_tv4 = Label(text="TV4").__self__
        ch_chooser_layout.add_widget(lb_tvp1)
        ch_chooser_layout.add_widget(cb_tvp1)
        ch_chooser_layout.add_widget(lb_tvp2)
        ch_chooser_layout.add_widget(cb_tvp2)
        ch_chooser_layout.add_widget(lb_tvppol)
        ch_chooser_layout.add_widget(cb_tvppol)
        ch_chooser_layout.add_widget(lb_tvpkul)
        ch_chooser_layout.add_widget(cb_tvpkul)
        ch_chooser_layout.add_widget(lb_tvpspo)
        ch_chooser_layout.add_widget(cb_tvpspo)
        ch_chooser_layout.add_widget(lb_polsat)
        ch_chooser_layout.add_widget(cb_polsat)
        ch_chooser_layout.add_widget(lb_tv4)
        ch_chooser_layout.add_widget(cb_tv4)

        ch_switch = Button(text="Przełącz").__self__
        ch_cancel = Button(text="Anuluj").__self__
        ch_cancel.on_press = lambda: channel_chooser.dismiss()
        ch_switch.on_press = lambda: chchannel(channel_chooser)
        ch_chooser_layout.add_widget(ch_switch)
        ch_chooser_layout.add_widget(ch_cancel)

        cb_tvp1.active = True

        channel_chooser = Popup(title="Zmień kanał", content=ch_chooser_layout, size_hint=(None, None), size=(600, 1110)).__self__

        main_layout = BoxLayout(padding=10, orientation='vertical').__self__
        tvp_fetch(100, 1, "TG1", False)

        page_control_layout = GridLayout(cols=3, row_force_default=True, row_default_height=120).__self__
        pagelabel = Label(text="Strona:").__self__

        pageinput.bind(text=on_text)
        navigate_btn = Button(text='Idź').__self__
        navigate_btn.on_press = lambda: navigate_callback(int(pageinput_val), 1, True)
        page_control_layout.add_widget(pagelabel)
        page_control_layout.add_widget(pageinput)
        page_control_layout.add_widget(navigate_btn)

        subpage_control_layout = GridLayout(cols=4, row_force_default=True, row_default_height=120).__self__
        subpagelabel = Label(text="Podstrona:").__self__
        subpageprev.on_press = lambda: navigate_callback(pobrana_strona, podstrona - 1, True)
        subpagenext.on_press = lambda: navigate_callback(pobrana_strona, podstrona + 1, True)
        subpage_control_layout.add_widget(subpagelabel)
        subpage_control_layout.add_widget(subpageprev)
        subpage_control_layout.add_widget(subpagecounter)
        subpage_control_layout.add_widget(subpagenext)

        navigation_layout = GridLayout(cols=2, row_force_default=True, row_default_height=120).__self__
        prevbutton = Button(text="Wstecz").__self__
        prevbutton.on_press = lambda: prev_page()
        homebutton = Button(text="Strona główna").__self__
        homebutton.on_press = lambda: navigate_callback(100, 1, True)
        navigation_layout.add_widget(prevbutton)
        navigation_layout.add_widget(homebutton)

        channelbutton = Button(text='Zmień kanał').__self__
        channelbutton.on_press = lambda: channel_chooser.open()

        controls_layout = GridLayout(cols=1, row_force_default=True, row_default_height=120).__self__
        controls_layout.add_widget(channelname)
        controls_layout.add_widget(page_control_layout)
        controls_layout.add_widget(subpage_control_layout)
        controls_layout.add_widget(navigation_layout)
        controls_layout.add_widget(channelbutton)

        main_layout.add_widget(screen)
        main_layout.add_widget(controls_layout)
        return main_layout


if __name__ == '__main__':
    app = TelegazetaExplorerApp()
    app.run()
