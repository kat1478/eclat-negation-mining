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
        """
        # TODO: Zaimplementować logikę
        print("Budowanie początkowych TID-list - do implementacji!")
        pass

    def transform(self):
        """
        Metoda zwracająca odkryte częste zbiory.
        """
        return self.frequent_itemsets