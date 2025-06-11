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
        self._discover_frequent_itemsets(self.tid_lists, k=1)
        
        print("Algorytm Eclat zakończył działanie.")
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
    
    def _discover_frequent_itemsets(self, item_tid_lists_k, k):
        """
        Rekurencyjnie odkrywa częste zbiory o rozmiarze k+1 na podstawie
        zbiorów o rozmiarze k.

        Args:
            item_tid_lists_k (dict): Słownik {item: tid_list} dla zbiorów o rozmiarze k.
                                     Dla k=1, item jest stringiem. Dla k>1, item jest frozensetem.
            k (int): Aktualny rozmiar itemsetów.
        """
        # Warunek stopu rekurencji: jeśli nie ma już itemsetów do rozszerzenia
        if not item_tid_lists_k:
            return

        min_transactions = self.min_support * self.num_transactions
        
        # Słownik na znalezione częste zbiory o rozmiarze k+1
        frequent_itemsets_k_plus_1 = {}

        # Używamy posortowanej listy kluczy, aby uniknąć duplikatów i powtórzeń
        # Np. połączymy {A} z {B}, ale nie połączymy później {B} z {A}
        items_k = sorted(list(item_tid_lists_k.keys()))

        for i in range(len(items_k)):
            for j in range(i + 1, len(items_k)):
                item_i = items_k[i]
                item_j = items_k[j]

                # Łączymy dwa itemsety w nowego kandydata
                # Dla k=1, łączymy dwa itemy w zbiór 2-elementowy
                # Dla k>1, łączymy dwa zbiory k-elementowe
                if k == 1:
                    candidate = frozenset([item_i, item_j])
                else: # k > 1
                    candidate = item_i.union(item_j)

                # Optymalizacja: jeśli kandydat ma zły rozmiar, pomijamy go
                # To się dzieje, gdy itemsety nie miały wspólnego prefixu
                if len(candidate) != k + 1:
                    continue
                
                # Obliczamy TID-listę kandydata przez przecięcie TID-list jego składowych
                tid_list_i = item_tid_lists_k[item_i]
                tid_list_j = item_tid_lists_k[item_j]
                candidate_tid_list = tid_list_i.intersection(tid_list_j) #serce Eclat - zamiast skanowac przecinamy dwa zbiory ID transakcji, szybkie

                # Sprawdzamy, czy kandydat jest częsty
                if len(candidate_tid_list) >= min_transactions:
                    frequent_itemsets_k_plus_1[candidate] = candidate_tid_list

        # Jeśli znaleziono jakieś częste zbiory, dodajemy je do głównego wyniku
        if frequent_itemsets_k_plus_1:
            # Aktualizujemy nasz główny słownik z wynikami
            for itemset, tid_list in frequent_itemsets_k_plus_1.items():
                self.frequent_itemsets[itemset] = len(tid_list)
            
            # Wywołujemy rekurencję dla nowo znalezionych zbiorów
            self._discover_frequent_itemsets(frequent_itemsets_k_plus_1, k + 1)
