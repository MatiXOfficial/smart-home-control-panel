# Smart Home Control Panel
Aplikacja pilota do sterowania urządzeniami inteligentnego domu stworzona w ramach kursu Programowanie w Języku Python 2019/20 na AGH.
------
Autor: Mateusz Kocot
-----------------------------------------------

# Cel i opis projektu
Celem projektu było stworzenie aplikacji pilota z interfejsem graficznym, za pomocą której będzie można wydawać polecenia przesyłane poprzez sieć do intelegentnego domu. Konfiguracja pilota wczytywana jest z pliku o formacie `json`. Polecenia przesyłane są do serwera MQTT. Pilot dzieli urządzenia na pokoje. Serwer publikuje i subskrybuje tematy postaci: `<przedrostek>/<pokój>/<urządzenie>/<typ komunikatu>` oraz ewentuanie `<przedrostek>/<temp>` dla zmian temperatury.
- `<przedrostek>` - odpowiedni przedrostek dodawany jest do publikacji (domyślnie `cmd`) i subskrypcji (domyślnie `var`). Pozwala na odróżnienie wiadomości wysyłanych od odbieranych. Uwaga! Aplikacja testowana była tylko w przypadku, gdy oba przedrostki były takie same. Wówczas pilot dokonywał zmian na podstawie wiadomości wysyłanych przez siebie lub inne piloty. Docelowo powinien on reagować na wiadomości wysyłane przez urządzenia. Stąd rozróżnienie obu przedrostków. 
- `<pokój>` - urządzenia podzielone są na pokoje.
- `<urządzenie>` - nazwa urządzenia.
- `<typ komunikatu>` pozwala serwerowi odróżnić komunikaty dla tego samego urządzenia o różnym celu (szczegóły niżej).

Domyślnie wartości `<pokój>` i `<urządzenie>` są tożsame z ich odpowiednimi nazwami podanymi w pliku konfiguracyjnym, ale można to zmienić.

# Instalacja
## Gotowe wydanie
W systemach Windows najprostszym sposobem na uruchomienie aplikacji jest pobranie najnowszego wydania (paczka *pilot.zip*). W paczce znajduje się plik wykonywalny `pilot.exe` oraz plik konfiguracyjny `config.json` (szczegóły niżej).

## Kod źródłowy
Drugim sposobem jest pobranie i uruchomienie kodu źródłowego napisanego w Pythonie. Do uruchomienia wymagany jest zainstalowany [Python 3](https://www.python.org/downloads/). Należy także zainstalować pakiet `paho-mqtt`:
```
pip install paho-mqtt
```
By włączyć aplikację, należy uruchomić plik `main.py` za pomocą interpretera Pythona:
```
python main.py
```

# Serwer MQTT
Aplikacja komunikuje się z serwerem MQTT, więc trzeba przygotować np. [Eclipse Mosquitto](https://mosquitto.org/download/). Do testów można wykorzystać serwer dostępny online, np: test.mosquitto.org.

# Plik konfiguracyjny
W pliku konfiguracyjnym `config.json` podawana jest konfiguracja pilota. Plik oparty jest o format json. Przykładowy wygląd pliku znajduje się niżej.

## Parametry
W pierwszym słowniku znajdują się następujące parametry:
- `"adres"` - adres serwera MQTT. Parametr ten nie musi zostać podany w pliku. Wówczas program poprosi o wpisanie adresu przy starcie.
- `"nazwa"` - nazwa użytkownika serwera MQTT. Parametr ten nie musi zostać podany w pliku. Wówczas program poprosi o wpisanie adresu przy starcie.
- `"publikacja"` - przedrostek dodawany do tematów publikowanych wiadomości. Parametr ten nie musi zostać podany w pliku. Wówczas brana pod uwagę będzie domyślna wartość `cmd`.
- `"subskrypcja"` - przedrostek dodawany do tematów subskrybowanych wiadomości. Parametr ten nie musi zostać podany w pliku. Wówczas brana pod uwagę będzie domyślna wartość `var`.
- `"temperatura"` - opcjonalny słownik. Po jego podaniu, w aplikacji będzie można zmieniać oczekiwaną temperaturę w °C. Słownik ten zawiera następujące klucze:
  - `"min"` - Wartość minimalna temperatury. Przy braku tego klucza, ustawiana na 15°C.
  - `"max"` - Wartość maksymalna temperatury. Przy braku tego klucza, ustawiana na 30°C.
  - `"krok"` - Wartość określająca zmianę temperatury po naciśnięciu przycisku. Przy braku tego klucza, ustawiana na 0.5°C.
  - `"start"` - Wartość początkowa temperatury. Przy braku tego klucza, ustawiana na średnią arytmetyczną wartości `"min"` i `"max"`.
- `"pokoje"` - słownik, którego kluczami są nazwy pokoi, a wartościami są słowniki zawierające urządzenia znajdujące się w danym pokoju. Kluczami tych słowników są nazwy urządzeń, a wartościami - atrybuty urządzenia (typ i jego wartości - szczegóły poniżej).

## Urządzenia i ich typy
Urządzenia określane są przez słownik zawierający przede wszystkim klucz `"typ"`. Możliwe typy urządzeń to:
- `przełącznik` - podstawowe urządzenie. Zawiera tylko przycisk do włączania i wyłączania. Może być wykorzystane do sterowania zwykłą lampą. Uwaga! Jest to domyślny typ. Gdy w pliku konfiguracyjnym nie będzie klucza `"typ"`, urządzenie zostanie uznane za przełącznik.
- `suwak` - rozbudowany przełącznik. Oprócz przycisku do włączania i wyłączania zawiera suwak określający np. natężenie światła w bardziej zaawansowanej lampie. Dodatkowe parametry:
  - `"min"` - określa minimalną wartość na suwaku. Domyślnie, tj. przy braku tego klucza - ustawiana na `1`.
  - `"max"` - określa maksymalną wartosć na suwaku. Musi zostać podany.
- `tv` - urządzenie, które oprócz włącznika zawiera przełącznik kanałów i głośności. Po kliknięciu na liczbę określającą kanał albo głośność można wybrać odpowiedni parametr wpisując liczbę w nowym oknie. Dodatkowe parametry:
  - `"kanały"` - liczba kanałów. Kanały rozpoczynają się od kanału pierwszego.
  - `"max głośność"` - maksymalna głośność. Głośność można wówczas ustawiać od `0` do `max głóśność`. Domyślnie,   tj. przy braku tego klucza - ustawiana na `100`.<br>
- `roleta` - zapewnia możliwość podnoszenia i opuszczania. Przy podnoszeniu oraz po podniesieniu, a także przy opuszczaniu oraz po opuszczeniu wyświetlają się odpowiednie komunikaty. Jeśli przedrostki publikacji i subskrypcji są takie same, oba komunikaty wyświetlą się niemal jednocześnie.

Dla każdego urządzenia może zostać podany także parametr `"temat"`. Wówczas fragment tematu `<pokój>/<urządzenie>` będzie ustawiony na to, co podał użytkownik. Ważne, by postać była taka sama (dwa słowa oddzielone ukośnikiem). Domyślnie do utworzenia tematu wykorzystane zostaną nazwy pokoju i urządzenia.

Typy komunikatów dla każdego urządzenia wyglądają następująco:
- `przełącznik`
  - `toggle` - odpowiedzialny za włączanie i wyłączanie.
- `suwak`
  - `toggle` - odpowiedzialny za włączanie i wyłączanie.
  - `slider` - odpowiedzialny za ustawienie suwaka.
- `tv`
  - `toggle` - odpowiedzialny za włączanie i wyłączanie.
  - `channel` - odpowiedzialny za zmianę kanału.
  - `volume` - odpowiedzialny za zmianę głóśności.
- `roleta`
  - `blind` - odpowiedzialny za podnoszenie i opuszczanie rolety.

## Przykład
Przykładowy wygląd pliku `config.json`:
```
{
    "adres" : "test.mosquitto.org",
    "publikacja" : "cmd",
    "subskrypcja" : "cmd",
    "temperatura" : {
        "min" : 15,
        "max" : 25,
        "start" : 21
    },

    "pokoje" : {
        "przedpokój" : {
            "lampka" : {
                "temat" : "salon/lampka"
            },
            "roleta" : {
                "typ" : "roleta"
            }
        },
        "salon" : {
            "lampa główna" : {
                "typ" : "przełącznik"
            },
            "lampa mała" : {},
            "telewizor" : {
                "typ" : "tv",
                "kanały" : 20
            },
            "roleta 1" : {
                "typ" : "roleta"
            },
            "roleta 2" : {
                "typ" : "roleta"
            }
        },
        "kuchnia" : {
            "lampa duża" : {},
            "oświetlenie kuchni" : {
                "max" : 6,
                "typ" : "suwak"
            }
        },
        "sypialnia" : {
            "lampka nocna" : {},
            "roleta" : {
                "typ" : "roleta"
            }   
        },
        "biuro" : {
            "podświetlenie led" : {
                "typ" : "suwak",
                "min" : 2,
                "max" : 10
            },
            "telewizor" : {
                "typ" : "tv",
                "kanały" : 1000,
                "max głośność" : 200
            }
        }
    }
}
```

## Opis przykładu
W powyższym przykładzie nie została podana `nazwa`. Program poprosi o podanie nazwy użytkownika przy uruchomieniu. Adres ustawiony jest na stronę `test.mosquitto.org`. Przy lokalnym uruchomieniu serwera, należy podać lokalny adres IP. Przedrostek `publikacji` i `subskrypcji` to `cmd`. Aplikacja pozwoli na zmianę temperatury za sprawą klucza `"temperatura"`. Nie podano wartości `kroku`, która zostanie ustawiona domyślnie na `0.5`. Urządzenia podzielone są na następujące pokoje:
- `przedpokój` zawiera:
  - `lampka` - przełącznik (domyślnie) o fragmencie tematu zmienionym na `"salon/lampka"`. Domyślnie byłoby to `"przedpokój/lampka"`.
  - `roleta` - typ `roleta`
- `salon` zawiera:
  - `lampa główna` - przełącznik
  - `lampa mała` - przełącznik
  - `telewizor` - typ `tv` o liczbie kanałów: 20 oraz domyślnej maksymalnej głośności: 100.
  - `roleta 1` - typ `roleta`
  - `roleta 2` - typ `roleta`
- `kuchnia` zawiera:
  - `lampa duża` - przełącznik
  - `oświetlenie kuchni` - typ `suwak` o minimalnej wartości ustawionej domyślnie na 1 oraz maksymalnej wartości: 6.
- `sypialnia` zawiera:
  - `lampka nocna` - przełącznik
  - `roleta` - typ `roleta`
- `biuro` zawiera:
  - `podświetlenie led` - typ `suwak` o minimalnej wartości ustawionej na 2 oraz maksymalnej wartości: 10.
  - `telewizor` - typ `tv` o liczbie kanałów: 1000 oraz domyślnej maksymalnej głośności: 200.

# Przykładowy wygląd programu

![alt text](readme_images/nazwa_okno.png "Okno z wyborem nazwy")

![alt text](readme_images/przedpokój_okno.png "Zakładka przedpokój")

![alt text](readme_images/salon_okno.png "Zakładka salon")

![alt text](readme_images/tv_okno.png "Okno służące do wpisywania liczby")

![alt text](readme_images/kuchnia_okno.png "Zakładka kuchnia")

![alt text](readme_images/kuchnia_okno_2.png "Zakładka kuchnia - włączone urządzenia")