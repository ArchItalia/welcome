#!/usr/bin/env python3
#
# Author :
# Date:
# Version 1.0.0:
# gtk3 glib2 pango gobject-introspection

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Pango


class ContentStyle:
    def __init__(self):
        self.font = 'Architalia'
        self.color = '#ffffff'

    def apply_to_label(self, label):
        label.override_font(Pango.FontDescription.from_string(self.font))
        label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_string(self.color))


class SidebarStyle:
    def __init__(self):
        self.color = "#333333"
        self.size = 12
        self.font_desc = Pango.FontDescription()

    def set_font(self, font):
        self.font_desc.set_family(font)

    def set_color(self, color):
        self.color = color

    def set_size(self, size):
        self.size = size
        self.font_desc.set_size(size * Pango.SCALE)

    def apply_to_sidebar(self, sidebar):
        context = sidebar.get_style_context()
        css_provider = Gtk.CssProvider()
        css = ".sidebar-row { color: %s; }" % self.color
        css_provider.load_from_data(css.encode())
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        for row in sidebar.get_children():
            self.apply_to_sidebar_row(row)

    def apply_to_sidebar_row(self, row):
        for child in row.get_children():
            if isinstance(child, Gtk.Label):
                font_markup = "<span font_desc=\"%s\"><b>%s</b></span>" % (self.font_desc.to_string(), child.get_text())
                child.set_markup(font_markup)


class SidebarItem(Gtk.ListBoxRow):
    def __init__(self, icon_path, title, description):
        super().__init__()

        # Creazione di un contenitore per l'icona e il testo
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        # Aggiunta dell'icona all'interno del contenitore
        icon_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_path, 24, 24, True)
        icon_image = Gtk.Image()
        icon_image.set_from_pixbuf(icon_pixbuf)
        hbox.pack_start(icon_image, False, False, 0)

        # Aggiunta del titolo e della descrizione all'interno del contenitore come etichette
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        title_label = Gtk.Label(label=title, xalign=0)
        title_label.set_markup("<b>%s</b>" % title)
        vbox.pack_start(title_label, False, False, 0)

        description_label = Gtk.Label(label=description, xalign=0)
        vbox.pack_start(description_label, False, False, 0)

        hbox.pack_start(vbox, False, False, 0)

        # Aggiunta del contenitore alla riga della barra laterale
        self.add(hbox)


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="")
        self.set_default_size(1000, 650)
        self.set_size_request(1000, 650)
        self.set_resizable(False)
        
        
        # Creazione della sidebar
        self.sidebar = Gtk.ListBox()
        self.sidebar.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.sidebar.connect("row-selected", self.on_sidebar_item_selected)

        # Impostazione della larghezza della sidebar
        self.sidebar.set_size_request(200, -1)

        # Aggiunta delle voci del menu alla sidebar
        sidebar_items = [
            {"icon_path": "/usr/share/welcome/icn/welcome.png", "title": "Welcome", "description": "About Core Linux"},
            {"icon_path": "/usr/share/welcome/icn/timeshift.png", "title": "Timeshift", "description": "First step"},
            {"icon_path": "/usr/share/welcome/icn/color-folders.png", "title": "Color Folders", "description": "Papirus folders"},
            {"icon_path": "/usr/share/welcome/icn/clean.png", "title": "Clean", "description": "System cleaner"}
        ]
        for item in sidebar_items:
            listbox_row = SidebarItem(item["icon_path"], item["title"], item["description"])
            self.sidebar.add(listbox_row)

        # Creazione del contenitore principale per sidebar e pagina di contenuto
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(main_box)

        # Aggiunta della sidebar al contenitore principale
        main_box.pack_start(self.sidebar, False, False, 0)

        # Creazione del contenitore per la pagina di contenuto
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.pack_start(content_box, True, True, 0)

        # Creazione delle pagine di contenuto
        self.pages = []

        # Creazione delle 6 pagine di contenuto
        # Pagina 1
        page1_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page1_box.set_margin_top(40)
        
        image = Gtk.Image.new_from_file('/usr/share/welcome/icn/core.png')
        page1_box.pack_start(image, False, False, 0)
        
        label1_0 = Gtk.Label()
        label1_0.set_markup("<span font_desc='Helvetica Bold 25' foreground='#000000' font_family='Helvetica'> </span>")
        label1_1 = Gtk.Label()
        label1_1.set_markup("<span font_desc='Architalia Bold 25' foreground='#d8dee9' font_family='Architalia'>Welcome to Core Linux!</span>")
        label1_2 = Gtk.Label()
        label1_2.set_markup("<span font_desc='Architalia 20' foreground='#d8dee9' font_family='Architalia'>Core Linux is a distribution based on Arch Linux</span>")
        label1_3 = Gtk.Label()
        label1_3.set_markup("<span font_desc='Architalia 14' foreground='#d8dee9' font_family='Architalia'>Core Linux is a project developed by the Italian community team of Architalia.</span>")
        link_button = Gtk.LinkButton.new_with_label("https://architalia.github.io/core", "https://architalia.github.io/core")
        page1_box.pack_start(label1_0, False, False, 0)
        page1_box.pack_start(label1_1, False, False, 0)
        page1_box.pack_start(label1_2, False, False, 0)
        page1_box.pack_start(label1_3, False, False, 0)
        page1_box.pack_start(link_button, False, False, 0)
        self.pages.append(page1_box)
        content_box.pack_start(page1_box, True, True, 0)
        
        # Pagina 2
        page2_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        label2_1 = Gtk.Label(label="Questa è la pagina 2.")
        label2_2 = Gtk.Label(label="Aggiungi qui tutte le etichette che vuoi.")
        page2_box.pack_start(label2_1, False, False, 0)
        page2_box.pack_start(label2_2, False, False, 0)
        self.pages.append(page2_box)
        content_box.pack_start(page2_box, True, True, 0)
        
        # Pagina 3
        page3_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        label3_1 = Gtk.Label(label="Questa è la pagina 3.")
        label3_2 = Gtk.Label(label="Aggiungi qui tutte le etichette che vuoi.")
        page3_box.pack_start(label3_1, False, False, 0)
        page3_box.pack_start(label3_2, False, False, 0)
        self.pages.append(page3_box)
        content_box.pack_start(page3_box, True, True, 0)
        
        # Pagina 4
        page4_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        label4_1 = Gtk.Label(label="Questa è la pagina 4.")
        label4_2 = Gtk.Label(label="Aggiungi qui tutte le etichette che vuoi.")
        page4_box.pack_start(label4_1, False, False, 0)
        page4_box.pack_start(label4_2, False, False, 0)
        self.pages.append(page4_box)
        content_box.pack_start(page4_box, True, True, 0)
        
        # Pagina 5
        page5_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        label5_1 = Gtk.Label(label="Questa è la pagina 5.")
        label5_2 = Gtk.Label(label="Aggiungi qui tutte le etichette che vuoi.")
        page5_box.pack_start(label5_1, False, False, 0)
        page5_box.pack_start(label5_2, False, False, 0)
        self.pages.append(page5_box)
        content_box.pack_start(page5_box, True, True, 0)
        
        # Pagina 6
        page6_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        label6_1 = Gtk.Label(label="Questa è la pagina 6.")
        label6_2 = Gtk.Label(label="Aggiungi qui tutte le etichette che vuoi.")
        page6_box.pack_start(label6_1, False, False, 0)
        page6_box.pack_start(label6_2, False, False, 0)
        self.pages.append(page6_box)
        content_box.pack_start(page6_box, True, True, 0)

        

        # Applicazione dello stile ai widget nella barra laterale.
        my_sidebar_style = SidebarStyle()
        my_sidebar_style.set_font('Architalia')
        my_sidebar_style.set_color('#333333')
        my_sidebar_style.set_size(12)
        my_sidebar_style.apply_to_sidebar(self.sidebar)

        # Mostra la prima pagina di contenuto all'avvio
        self.pages[0].show()

    def on_sidebar_item_selected(self, listbox, listbox_row):
        # Nasconde tutte le pagine e mostra solo quella selezionata dalla sidebar
        for page in self.pages:
            page.hide()

        selected_page_index = listbox_row.get_index()
        self.pages[selected_page_index].show()


win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()