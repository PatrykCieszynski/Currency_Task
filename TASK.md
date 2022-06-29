##Opis potrzeby użytkownika końcowego
Sprzedawca posiada sklep e-commerce z różnymi produktami. Do tej pory handel był realizowany na
terenie Polski. Sprzedawca chciałby wysyłać towary do krajów Unii Europejskiej oraz do Stanów
Zjednoczonych. Pojawiała się zatem u niego potrzeba akceptacji płatności w dolarach amerykańskich
(USD) oraz w Euro. Kupujący musi wiedzieć ile towar kosztuje w danej walucie.
Sprzedawca potrzebuje rozwiązania, które cyklicznie raz dziennie lub na żądanie pobierze aktualny
kurs walut z Narodowego Banku Polskiego i dokona aktualizacji cen dla produktów w bazie danych.
##Wstępna konfiguracja środowiska
1. Należy zainstalować bazę danych MySQL i utworzyć bazę o nazwie mydb.
2. Do bazy danych zaimportować schemat sklepu ecommerce, który jest dostępny pod
adresem: https://raw.githubusercontent.com/abdelatifsd/E-commerce-DatabaseProject/master/3%20-%20Structure.sql
3. Następnie należy zaimportować testowe dane do bazy danych, które są dostępne pod
adresem: https://raw.githubusercontent.com/abdelatifsd/E-commerce-DatabaseProject/master/4%20-%20Population.sql
Uwaga: dane należy ładować w kolejności od góry do dołu, transakcja po transakcji z uwagi
na to, że niektóre klienty np. MySQL Workbench ładują dane jednocześnie i może wtedy
wystąpić błąd importu.
##Wymagania funkcjonalne
1. W tabeli Product należy dodać dwie nowe
kolumny: UnitPriceUSD, UnitPriceEuro. Komentarz - w systemie produkcyjnym nie jest to
najlepsza metoda aby takie informacje dodawać bezpośrednio w tabeli product. Z reguły
ceny dla różnych walut powinny być trzymane np. w cache lub powinna być jedna tabela
typu Currency i w niej aktualny kurs waluty i cena wtedy byłaby dynamicznie przeliczana.
Jednak na potrzeby tego ćwiczenia wystarczy dodać dwie wymienione wcześniej kolumny.
2. Utworzyć skrypt w języku Python, który połączy się po REST API do Narodowego Banku
Polskiego i pobierze aktualny kurs waluty dla USD i Euro. API do NBP znajduje się
tutaj: http://api.nbp.pl/en.html.
3. Następnie skrypt ten po pobraniu kursów powinien wykonać aktualizację cen wszystkich
produktów w bazie danych (kolumna UnitPriceUSD, UnitPriceEuro).
4. Następnie skrypt powinien mieć oddzielny tryb działania, który na żądanie wygeneruje
Excela z listą wszystkich produktów w bazie danych z następującymi kolumnami:
a. ProductID
b. DepartmentID
c. Category
d. IDSKU
e. ProductName
f. Quantity
g. UnitPrice
h. UnitPriceUSD
i. UnitPriceEuro
j. Ranking
k. ProductDesc
l. UnitsInStock
m. UnitsInOrder
Wymagania poza funkcjonalne
1. Skrypt powinien być napisany obiektowo jeżeli to możliwe.
2. Kod w skrypcie powinien być udokumentowany według uznania.
3. Rozwiązanie należy wrzucić na konto GitHub.
4. Zmieniony schemat bazy danych należy wyeksportować w formie sql i także wrzucić na
GitHub.
5. Skrypt powinien wykorzystywać moduł logging do tego aby logować operację z działania do
pliku logu.
6. Skrypt powinien także obsłużyć wyjątek np. gdy API NBP nie będzie dostępne lub jak baza
danych nie będzie dostępna lub jak wystąpi inny błąd. Wtedy błędy powinny być logowane
do pliku logu.
7. Opcjonalnie skrypt może być stworzony w standardzie paczki python, którą można będzie
zainstalować za pomocą komendy: pip install <module_name>.whl.
Czas realizacji zadania 30/06/2022 do godziny 16:00. Jeżeli nie uda się całościowo ukończyć zadania,
proszę o wrzucenie kodu, który udało się wykonać.