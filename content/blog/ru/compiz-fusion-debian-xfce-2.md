Title: Установка Compiz Fusion (Debian + Xfce)
Date: 2008-02-11T01:27:00
Tags: compiz fusion, debian, emerald, xfce, linux
Slug: 50
Feed: false

В этой заметке я опишу процесс установки и базовой настройки оконного менеджера Compiz Fusion в Debian с рабочим окружением Xfce. [Ранее я писал об этом](http://cornelius.net.ru/blog/compiz-fusion-debian-xfce), но время не стоит на месте, и те инструкции уже устарели.

В данный момент Compiz Fusion вошёл в состав Debian Lenny (testing), поэтому подключать дополнительные репозитории вам не придётся (если только вы не хотите использовать оконный декоратор Emerald, о чём ниже).

Итак, приступим…

<!-- more -->

Прежде всего установите необходимые пакеты:

    sudo aptitude install compiz-core compiz-plugins compizconfig-settings-manager compiz-fusion-plugins-main

Затем вам следует определиться с выбором оконного декоратора. *Оконный декоратор* – это программа, которая рисует рамки окон и кнопки типа “Закрыть окно”. Существует три оконных декоратора:

* gtk-window-decorator (GWD)
* kde-window-decorator
* emerald

*kde-window-decorator* мы рассматривать не будем, так как к Xfce он не имеет никакого отношения. А вот *GWD* и *emerald* рассмотрим поподробнее.

## gtw-window-decorator

Этот оконный декоратор основан на Metacity (оконный менеджер Gnome) со всеми вытекающими последствиями: он зависит от *libmetacity* и *gconf*. Настройки GWD хранятся в gconf, в качестве темы оформления окна используются темы Metacity.

Для установки GWD выполните следующую команду:

    sudo aptitude install compiz-gtk

Для изменения настроек GWD, а также для выбора темы Metacity можно воспользоваться командой:

    gconf-editor
    
{% image 40 original "GConf Editor - GTK Window Decorator" %}

{% image 41 original "GConf Editor - Metacity" %}

## Emerald

Этот оконный декоратор не зависит от библиотек Gnome, имеет собственную программу для настройки и выбора темы. Но у него есть существенный “недостаток” – в составе Debian Lenny его нет. Однако существует сторонний репозиторий, которым вы можете воспользовать для установки Emerald. Для этого добавьте в файл /etc/apt/sources.list следующую строку:

    deb http://download.tuxfamily.org/shames/debian-sid/desktopfx/unstable/ ./
    
Установите GPG ключ для этого репозитория:

    wget http://download.tuxfamily.org/shames/A42A6CF5.gpg -O- | sudo apt-key add -
    
и обновите списки пакетов:

    sudo aptitude update

ВНИМАНИЕ! Этот репозиторий не является официальным репозиторием Debian – используйте его на свой страх и риск.

Для установки Emerald выполните:

    sudo aptitude install emerald emerald-themes

Теперь нужно настроить compiz для использования того или иного оконного декоратора. Для этого запустите программу настройки compiz:

    ccsm
    
Откройте раздел “Оформление окна” (в секции Effects). В строке “Команда” введите

    gtk-window-decorator --replace
    
если вы хотите использовать GWD, или

    emerald --replace

если вы хотите использовать Emerald.

{% image 42 original "Compiz Settings - Window Decoration" %}

Теперь соответствующий оконный декоратор будет запускаться вместе с compiz.

Настало время протестировать, работает ли compiz. Запустите команду:

    compiz --replace
    
Если всё в порядке, то вы должны увидеть, как изменились рамки у окон. Если рамки окон просто исчезли, то не работает либо compiz, либо оконный декоратор. В этом случае вам надо обратится к [списку наиболее распространённых проблем](http://wiki.compiz-fusion.org/FAQ).

Если же всё прошло успешно, то остаётся сделать так, чтобы в начале сеанса Xfce запускался не стандартный оконный менеджер *xfwm4*, а *compiz*. Для этого создайте файл `~/.config/autostart/compiz.desktop` со следующим содержимым:

    [Desktop Entry]
    Encoding=UTF-8
    Version=0.9.4
    Type=Application
    Name=compiz
    Comment=
    Exec=compiz --replace
    StartupNotify=false
    Terminal=false
    Hidden=false
    
Это файл автозапуска compiz.

**Обновлено:** Также Compiz можно запускать с помощью утилиты **fusion-icon** из одноимённого пакета. В этом случае вместо команды `compiz --replace` надо запускать `fusion-icon`. Эта утилита висит в трее и позволяет выбирать и автоматически запускать оконный менеджер/декоратор. Пакет fusion-icon совсем недавно появился в Debian sid и должен скоро мигрировать в testing.

Затем выполните команду

    killall xfwm4
    
и завершите сеанс с сохранением сессии. Теперь при начале нового сеанса xfwm4 запускаться не будет.

Для установки дополнительных плагинов *compiz fusion* выполните:

    sudo aptitude install compiz-fusion-plugins-extra
    
Напоследок несколько ссылок на тему Compiz Fusion:

* [Сайт Compiz Fusion](http://www.compiz-fusion.org/)
* [Wiki Compiz Fusion](http://wiki.compiz-fusion.org/)
* [Темы для Metacity](http://compiz-themes.org/index.php?xcontentmode=101)
* [Темы для Emerald](http://compiz-themes.org/index.php?xcontentmode=103)
