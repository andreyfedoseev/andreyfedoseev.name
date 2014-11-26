Title: Как поменять значения кнопок на клавиатуре (на Маке)
Date: 2011-12-24T08:54:00
Tags: mac
Slug: 60/kak-pomenyat-znacheniya-knopok-na-klaviatura-na-ma
Feed: false

Когда у меня была писишная клавиатура, я активно пользовался цифровым блоком, который расположен справа. Но не для набора цифр, а для перемещения по тексту туда-сюда с помощью стрелок и кнопок Home/End и PgUp/PgDown. Ещё там были кнопки Enter и Del, так что можно было выполнять кучу разных действий, вообще не перемещая руку .

Для мака я специально купил полноразмерную клавиатуру с цифровым блоком, но обнаружил, что там есть только цифры. Никаких стрелок и всего остального.

![Apple20Aluminium20ISO20International20English](/images/Apple20Aluminium20ISO20International20English.png)

Целый год я бился, чтобы найти способ поменять значения этих кнопок и, наконец-то, нашёл его.

Способ этот называется [KeyRemap4MacBook](http://pqrs.org/macosx/keyremap4macbook/index.html) (пусть название вас не смущает, эта программа работает со всеми маками, а не только с макбуками). Сайт программы выглядит очень красноглазо – как раз то, что мне надо!

Так выглядят окно настроек этой программки:

![keyremap](/images/keyremap.png)

Кнопка «Reload XML», упоминания Emacs и X11 сразу выдают в ней продукт, написанный программистом для программистов, а значит для меня. На скриншоте видна куча предустановок, которые можно включать и выключать галочками. Кроме этого, можно создавать свои собственные настройки, которые описываются в специальном файле [private.xml](http://pqrs.org/macosx/keyremap4macbook/xml.html). С помощью этого файла можно переназначить вообще все кнопки.

Формат этого файла достаточно простой. Значения кнопок в нём обозначаются специальными [ключевыми словами](https://github.com/tekezo/KeyRemap4MacBook/blob/master/src/core/bridge/keycode/data/KeyCode.data), либо цифровыми кодами. Для того, чтобы узнать цифровой код конкретной кнопки, в составе программы есть утилита EventViewer (вызывается через значок программы в панели меню). Эта утилита отображает код кнопки, которую вы нажимаете в данный момент. Причём код отображается в шестнадцатеричном виде, который вам придётся самостоятельно перевести в десятичный. Ну разве не прелесть?

Ниже приведён мой файл private.xml.

    #!xml
    <?xml version="1.0"?>
    <root>    
      <item>      
        <name>Fix Numpad</name>
        <identifier>fixnumpad</identifier>
    
        <!-- Стрелки и кнопки Home,End,PgUp,PgDown -->
        <autogen>--KeyToKey-- KeyCode::KEYPAD_1, KeyCode::END</autogen>
        <autogen>--KeyToKey-- KeyCode::KEYPAD_2, KeyCode::CURSOR_DOWN</autogen>
        <autogen>--KeyToKey-- KeyCode::KEYPAD_3, KeyCode::PAGEDOWN</autogen>
        <autogen>--KeyToKey-- KeyCode::KEYPAD_4, KeyCode::CURSOR_LEFT</autogen>
        <autogen>--KeyToKey-- KeyCode::KEYPAD_6, KeyCode::CURSOR_RIGHT</autogen>
        <autogen>--KeyToKey-- KeyCode::KEYPAD_7, KeyCode::HOME</autogen>
        <autogen>--KeyToKey-- KeyCode::KEYPAD_8, KeyCode::CURSOR_UP</autogen>
        <autogen>--KeyToKey-- KeyCode::KEYPAD_9, KeyCode::PAGEUP</autogen>
    
        <!-- Точка на цифровом блоке работает как Del -->
        <autogen>--KeyToKey-- KeyCode::KEYPAD_DOT, KeyCode::FORWARD_DELETE</autogen>

        <!-- Сочетание Shift+0 на цифровом блоке работает как Command+V -->
        <autogen>--KeyToKey-- KeyCode::KEYPAD_0, ModifierFlag::SHIFT_L,
                              KeyCode::V, ModifierFlag::COMMAND_L</autogen>
      </item>
    </root>

Как видите, различные модификаторы типа Shift, Control или Command тоже поддерживаются.
