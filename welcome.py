#!/usr/bin/env python3
#
# Author :
# Date:
# Version 1.0.0:
# gtk3 glib2 pango gobject-introspection

import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Pango
import cairo

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

        
        # Pagina 1 welcome
        page1_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page1_box.set_margin_top(40)
        
        output = subprocess.check_output('uname -r', shell=True)
        kernel = output.decode('utf-8').strip()
        image = Gtk.Image.new_from_file('/usr/share/welcome/icn/core.png')
        page1_box.pack_start(image, False, False, 0)
        
        label1_0 = Gtk.Label()
        label1_0.set_markup("<span font_desc='Helvetica Bold 25' foreground='#000000' font_family='Helvetica'> </span>")
        label1_1 = Gtk.Label()
        label1_1.set_markup("<span font_desc='Architalia Bold 25' foreground='#d8dee9' font_family='Architalia'>Welcome to Core Linux!</span>")
        label1_2 = Gtk.Label()
        label1_2.set_markup("<span font_desc='Architalia 20' foreground='#d8dee9' font_family='Architalia'>Core Linux is a distribution based on Arch Linux</span>")
        label1_3 = Gtk.Label()
        label1_3.set_markup("<span font_desc='Architalia 14' foreground='#81a1c1' font_family='Architalia'>Core Linux is a project developed by the Italian community team of Architalia.</span>")
        link_button0 = Gtk.LinkButton.new_with_label("", "")
        link_button = Gtk.LinkButton.new_with_label("https://architalia.github.io/core", "Web Site Core Linux")
        link_button2 = Gtk.LinkButton.new_with_label("https://architalia.github.io/site", "Web Site Architalia")
        link_button3 = Gtk.LinkButton.new_with_label("https://gitlab.com/architalialinux/ai-repo", "Repository")
        label1_4 = Gtk.Label()
        label1_4.set_markup("<span font_desc='Helvetica Bold 25' foreground='#000000' font_family='Helvetica'> </span>")
        label1_5a = Gtk.Label()
        label1_5a.set_markup(f"<span font_desc='Architalia 14' foreground='#ebcb8b' font_family='Architalia'>Kernel {kernel}</span>")
        label1_5 = Gtk.Label()
        label1_5.set_markup("<span font_desc='Architalia 14' foreground='#d8dee9' font_family='Architalia'>Core Linux 2023.08 Beta</span>")
        label1_6 = Gtk.Label()
        label1_6.set_markup("<span font_desc='Architalia 14' foreground='#81a1c1' font_family='Architalia'>Developed by Jonathan Sanfilippo, Klod cripta.</span>")
        page1_box.pack_start(label1_0, False, False, 0)
        page1_box.pack_start(label1_1, False, False, 0)
        page1_box.pack_start(label1_2, False, False, 0)
        page1_box.pack_start(label1_3, False, False, 0)

        page1_box.pack_start(link_button0, False, False, 0)
        page1_box.pack_start(link_button, False, False, 0)
        page1_box.pack_start(link_button2, False, False, 0)
        page1_box.pack_start(link_button3, False, False, 0)
        page1_box.pack_start(label1_4, False, False, 0)
        page1_box.pack_start(label1_5a, False, False, 0)
        page1_box.pack_start(label1_5, False, False, 0)
        page1_box.pack_start(label1_6, False, False, 0)
        self.pages.append(page1_box)
        content_box.pack_start(page1_box, True, True, 0)
        
        # Pagina 2 timeshift
        page2_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page2_box.set_margin_top(40)
        
        image = Gtk.Image.new_from_file('/usr/share/welcome/icn/timeshift.png')
        page2_box.pack_start(image, False, False, 0)

        
        label2_1 = Gtk.Label()
        label2_1.set_markup("<span font_desc='Architalia Bold 25' foreground='#d8dee9' font_family='Architalia'>Timeshift</span>")
        label2_2 = Gtk.Label()
        label2_2.set_markup("<span font_desc='Architalia Bold 14' foreground='#d8dee9' font_family='Architalia'>System restore tool for Linux</span>")
        label2_0 = Gtk.Label()
        label2_0.set_markup("<span font_desc='Helvetica Bold 25' foreground='#000000' font_family='Helvetica'> </span>")
        label2_3 = Gtk.Label()
        label2_3.set_markup("<span font_desc='Architalia 14' foreground='#d8dee9' font_family='Architalia'>Creates filesystem snapshots using rsync+hardlinks, or BTRFS snapshots.</span>")
        label2_4 =Gtk.Label()
        label2_4.set_markup("<span font_desc='Architalia 14' foreground='#81a1c1' font_family='Architalia'>A minimum of two daily and two boot snapshots are racommended.</span>")
        label2_5 =Gtk.Label()
        label2_5.set_markup("<span font_desc='Architalia 14' foreground='#ebcb8b' font_family='Architalia'>If anything breaks, you can then restore your computer to its previous working state.</span>")
        label2_00 = Gtk.Label()
        label2_00.set_markup("<span font_desc='Helvetica Bold 40' foreground='#000000' font_family='Helvetica'> </span>")
        
        button = Gtk.Button.new_with_label('Timeshift Launch')
        button.connect('clicked', lambda _: subprocess.check_call('timeshift-launcher', shell=True))
        button.set_size_request(200, 50) 
        
        page2_box.pack_start(label2_1, False, False, 0)
        page2_box.pack_start(label2_2, False, False, 0)
        page2_box.pack_start(label2_0, False, False, 0)
        page2_box.pack_start(label2_3, False, False, 0)
        page2_box.pack_start(label2_4, False, False, 0)
        page2_box.pack_start(label2_5, False, False, 0)
        page2_box.pack_start(label2_00, False, False, 0)
        page2_box.pack_start(button, False, False, 10)



        self.pages.append(page2_box)
        content_box.pack_start(page2_box, True, True, 0)
        
        # Pagina 3 color folders
        page3_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page3_box.set_margin_top(40)
        
        command_output = subprocess.check_output('papirus-folders -l --theme Papirus-Dark | grep ">"', shell=True)
        folder = command_output.decode("utf-8")

        image0 = Gtk.Image.new_from_file('/usr/share/welcome/icn/color-folders.png')
        image = Gtk.Image.new_from_file('/usr/share/icons/Papirus-Dark/64x64/places/folder-favorites.svg')
        

        label3_000 = Gtk.Label()
        label3_000.set_markup("<span font_desc='Helvetica Bold 10' foreground='#000000' font_family='Helvetica'> </span>")
        label3_1 = Gtk.Label()
        label3_1.set_markup("<span font_desc='Architalia Bold 25' foreground='#d8dee9' font_family='Architalia'>Color Folders</span>")
        label3_2 = Gtk.Label()
        label3_2.set_markup("<span font_desc='Architalia Bold 14' foreground='#d8dee9' font_family='Architalia'>Choose your favorite color</span>")
        label3_0 = Gtk.Label()
        label3_0.set_markup("<span font_desc='Helvetica Bold 25' foreground='#000000' font_family='Helvetica'> </span>")
        label3_3 = Gtk.Label()
        label3_3.set_markup("<span font_desc='Architalia 14' foreground='#d8dee9' font_family='Architalia'>Use Color Folders to change the style of your Papirus folders.</span>")
        label3_4 =Gtk.Label()
        label3_4.set_markup("<span font_desc='Architalia 14' foreground='#81a1c1' font_family='Architalia'>There are 45 different color types available for your Papirus folders.</span>")
        label3_5 =Gtk.Label()
        label3_5.set_markup("<span font_desc='Architalia 14' foreground='#ebcb8b' font_family='Architalia'>To apply the selected color to the desktop icons,</span>")
        label3_6 =Gtk.Label()
        label3_6.set_markup("<span font_desc='Architalia 14' foreground='#ebcb8b' font_family='Architalia'>right-click on the desktop after choosing your preferred theme.</span>")
        label3_99 = Gtk.Label()
        label3_99.set_markup(f"<span font_desc='Architalia 12' foreground='#d8dee9' font_family='Architalia'>Current color{folder}</span>")
        label3_00 = Gtk.Label()
        label3_00.set_markup("<span font_desc='Helvetica Bold 40' foreground='#000000' font_family='Helvetica'> </span>")
        
        button = Gtk.Button.new_with_label('Color Folders Launch')
        button.connect('clicked', lambda _: subprocess.check_call(["gnome-terminal", "--", "/usr/bin/color-folders"], shell=False))
        button.set_size_request(200, 50)
        
        page3_box.pack_start(image0, False, False, 0)
        page3_box.pack_start(label3_000, False, False, 0)
        page3_box.pack_start(label3_1, False, False, 0)
        page3_box.pack_start(label3_2, False, False, 0)
        page3_box.pack_start(label3_0, False, False, 0)
        page3_box.pack_start(label3_3, False, False, 0)
        page3_box.pack_start(label3_4, False, False, 0)
        page3_box.pack_start(label3_5, False, False, 0)
        page3_box.pack_start(label3_6, False, False, 0)
        page3_box.pack_start(label3_00, False, False, 0)
        page3_box.pack_start(image, False, False, 0)
        page3_box.pack_start(label3_99, False, False, 0)
        page3_box.pack_start(button, False, False, 10)



        self.pages.append(page3_box)
        content_box.pack_start(page3_box, True, True, 0)
        
                # Pagina 4 clean
        page4_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page4_box.set_margin_top(40)
        
        

        image0 = Gtk.Image.new_from_file('/usr/share/welcome/icn/clean.png')
        

        label4_000 = Gtk.Label()
        label4_000.set_markup("<span font_desc='Helvetica Bold 10' foreground='#000000' font_family='Helvetica'> </span>")
        label4_1 = Gtk.Label()
        label4_1.set_markup("<span font_desc='Architalia Bold 25' foreground='#d8dee9' font_family='Architalia'>Clean</span>")
        label4_2 = Gtk.Label()
        label4_2.set_markup("<span font_desc='Architalia Bold 14' foreground='#d8dee9' font_family='Architalia'>System Cleaner</span>")
        label4_0 = Gtk.Label()
        label4_0.set_markup("<span font_desc='Helvetica Bold 25' foreground='#000000' font_family='Helvetica'> </span>")
        label4_3 = Gtk.Label()
        label4_3.set_markup("<span font_desc='Architalia 14' foreground='#d8dee9' font_family='Architalia'>Clean is a tool created by the Core Linux team developers for system maintenance</span>")
        label4_4 =Gtk.Label()
        label4_4.set_markup("<span font_desc='Architalia 14' foreground='#81a1c1' font_family='Architalia'>to remove orphan packages, package cache, user cache, and trash.</span>")
        label4_6 =Gtk.Label()
        label4_6.set_markup("<span font_desc='Architalia 14' foreground='#ebcb8b' font_family='Architalia'>Just type the clean command or use the application in the menu.</span>")
        label4_00 = Gtk.Label()
        label4_00.set_markup("<span font_desc='Helvetica Bold 40' foreground='#000000' font_family='Helvetica'> </span>")
        
        button = Gtk.Button.new_with_label('Clean Launch')
        button.connect('clicked', lambda _: subprocess.check_call(["gnome-terminal", "--", "/usr/bin/clean"], shell=False))
        button.set_size_request(200, 50)
        
        page4_box.pack_start(image0, False, False, 0)
        page4_box.pack_start(label4_000, False, False, 0)
        page4_box.pack_start(label4_1, False, False, 0)
        page4_box.pack_start(label4_2, False, False, 0)
        page4_box.pack_start(label4_0, False, False, 0)
        page4_box.pack_start(label4_3, False, False, 0)
        page4_box.pack_start(label4_4, False, False, 0)
        page4_box.pack_start(label4_6, False, False, 0)
        page4_box.pack_start(label4_00, False, False, 0)
        page4_box.pack_start(button, False, False, 10)



        self.pages.append(page4_box)
        content_box.pack_start(page4_box, True, True, 0)
        

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