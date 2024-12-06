Obchodní bot
Tento program implementuje obchodní strategii založenou na křížení průměrů. Využívá Alpaca API pro načítání historických dat o akciích a provádí backtest s použitím této strategie pro generování nákupních a prodejních signálů.

Demo
Vytvořil jsem spustitelný soubor (.exe) tohoto programu pro snadnou distribuci. Můžete si stáhnout a spustit tento soubor přímo bez potřeby nastavovat Python prostředí. Program vás vyzve k zadání symbolu akcie (např. TSLA), následně stáhne historická data a provede backtest s použitím obchodní strategie na základě křížení průměrů.

Jak to funguje
Vstup: Po spuštění programu (nebo .exe souboru) budete vyzváni k zadání symbolu akcie (např. TSLA pro Tesla).

Strategie:

Krátkodobýprůměr: Používá okno o délce 21 period.
Dlouhodobýprůměr: Používá okno o délce 100 period.
Obchodní logika:

Nákupní signál: Když krátkodobýprůměr překročí dlouhodobýprůměr směrem nahoru, program vygeneruje nákupní signál.
Prodejní signál: Když krátkodobýprůměr překročí dlouhodobýprůměr směrem dolů, program vygeneruje prodejní signál.
Strategie provádí obchody pouze mezi 15:00 (3 PM) a 21:00 (9 PM), jak je specifikováno v programu.

Výstup:

Program vypíše podrobné informace o nákupních a prodejních signálech, včetně času a ceny obchodu.
Také vypočítá celkový zisk nebo ztrátu ze všech provedených obchodů během backtestu.
Vizualizace: Po dokončení backtestu program zobrazí graf, který ukazuje jak bot nakupoval a prodával a kdy.

Distribuce a cena  
Distribuce tohoto produktu bude probíhat prostřednictvím webové platformy, kde se uživatel zaregistruje a zakoupí produkt formou měsíčního předplatného. Po zakoupení bude uživatel požádán o zadání API klíče svého poskytovatele akcií (např. Alpaca), aby mohl použít bota pro obchodování.

Uživatel bude mít možnost kdykoliv zapnout nebo vypnout bota prostřednictvím uživatelského rozhraní. Bot poběží na mém serveru, takže uživatel nemusí mít vlastní infrastrukturu.

Cena tohoto řešení bude velmi konkurenceschopná, protože nabízím nižší měsíční poplatek než většina konkurence, která má obvykle vysoké ceny. Díky této nižší ceně bude uživatel schopen dosáhnout vyššího zisku i s menším počátečním kapitálem, protože náklady na používání bota nebudou vysoké.
