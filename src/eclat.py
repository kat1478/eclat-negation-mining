# src/eclat.py

class Eclat:
    """
    Implementacja algorytmu Eclat do odkrywania częstych zbiorów elementów,
    z rozszerzeniem o obsługę literałów negowanych.
    """
    def __init__(self, min_support=0.01, use_negation=False):
        """
        Konstruktor klasy.

        Args:
            min_support (float): Minimalny próg wsparcia (wartość od 0 do 1).
            use_negation (bool): Czy algorytm ma uwzględniać literały negowane.
        """
        self.min_support = min_support
        self.use_negation = use_negation
        self.transactions = None
        self.num_transactions = 0
        self.frequent_itemsets = None
        self.tid_lists = None

    def fit(self, transactions):
        """
        Główna metoda, która uruchamia algorytm na podanym zbiorze transakcji.

        Args:
            transactions (list of lists): Lista transakcji, gdzie każda transakcja
                                          to lista produktów.
        """
        self.transactions = transactions
        self.num_transactions = len(transactions)
        
        # Krok 1: Zbuduj TID-listy dla pojedynczych, częstych itemów
        self._build_initial_tid_lists()
        
        # Krok 2: Rekurencyjnie odkrywaj częste zbiory
        
        
        print("Algorytm Eclat (fit) - do implementacji!")
        return self

    def _build_initial_tid_lists(self):
        """
        Metoda prywatna do tworzenia początkowych list identyfikatorów transakcji (TID-list)
        dla pojedynczych produktów, które spełniają próg min_support.

        Na tym etapie obsługujemy tylko literały pozytywne.
        """
        # Obliczamy minimalną liczbę transakcji, jaką musi mieć item, by być częstym
        min_transactions = self.min_support * self.num_transactions

        temp_tid_lists = {}
        # Iterujemy po każdej transakcji z jej indeksem (TID)
        for tid, transaction in enumerate(self.transactions):
            for item in transaction:
                # Jeśli itemu nie ma jeszcze w naszej mapie, tworzymy dla niego pusty zbiór
                if item not in temp_tid_lists:
                    temp_tid_lists[item] = set()
                # Dodajemy ID transakcji do zbioru dla danego itemu
                temp_tid_lists[item].add(tid)
        
        # Filtrujemy TID-listy, zostawiając tylko te dla częstych itemów
        # Używamy słownika składanego (dictionary comprehension) dla zwięzłości
        self.tid_lists = {
            item: tids
            for item, tids in temp_tid_lists.items()
            if len(tids) >= min_transactions
        }

        # Inicjalizujemy zbiór częstych itemsetów
        # Na razie zawiera on tylko pojedyncze, częste itemy
        # Używamy frozenset, ponieważ klucze w słowniku muszą być niemutowalne
        self.frequent_itemsets = {
            frozenset([item]): len(tids)
            for item, tids in self.tid_lists.items()
        }

        print(f"Zbudowano początkowe TID-listy. Liczba częstych pojedynczych itemów: {len(self.tid_lists)}")

    def transform(self):
        """
        Metoda zwracająca odkryte częste zbiory.
        """
        return self.frequent_itemsets