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
        dla pojedynczych literałów (pozytywnych i/lub negowanych), które spełniają próg min_support.
        WERSJA ZOPTYMALIZOWANA PAMIĘCIOWO.
        """
        min_transactions = self.min_support * self.num_transactions
        
        temp_positive_tid_lists = {}
        for tid, transaction in enumerate(self.transactions):
            for item in transaction:
                if item not in temp_positive_tid_lists:
                    temp_positive_tid_lists[item] = set()
                temp_positive_tid_lists[item].add(tid)

        self.tid_lists = {}
        
        # Najpierw znajdujemy i przechowujemy częste literały POZYTYWNE
        frequent_positives = {}
        for item, tids in temp_positive_tid_lists.items():
            if len(tids) >= min_transactions:
                frequent_positives[item] = tids
                self.tid_lists[(item, '+')] = tids

        # Jeśli opcja negacji jest włączona, dodajemy częste literały NEGOWANE
        if self.use_negation:
            all_tids = set(range(self.num_transactions))
            
            # *** KLUCZOWA ZMIANA: Iterujemy TYLKO po częstych pozytywnych ***
            # Zamiast generować negacje dla 16k itemów, robimy to tylko dla kilkudziesięciu.
            for item, tids in frequent_positives.items():
                negated_tids = all_tids - tids
                if len(negated_tids) >= min_transactions:
                    self.tid_lists[(item, '-')] = negated_tids

        self.frequent_itemsets = {
            frozenset([literal]): len(tids)
            for literal, tids in self.tid_lists.items()
        }

        print(f"Zbudowano początkowe TID-listy. Liczba częstych pojedynczych literałów: {len(self.tid_lists)}")

    def transform(self):
        """
        Metoda zwracająca odkryte częste zbiory.
        """
        return self.frequent_itemsets
    
    def _discover_frequent_itemsets(self, item_tid_lists_k, k):
        """
        Rekurencyjnie odkrywa częste zbiory o rozmiarze k+1 na podstawie
        zbiorów o rozmiarze k. Wersja uniwersalna, obsługująca krotki (item, sign).
        """
        if not item_tid_lists_k:
            return

        min_transactions = self.min_support * self.num_transactions
        frequent_itemsets_k_plus_1 = {}

        # Sortujemy literały. Python domyślnie posortuje krotki najpierw po pierwszym elemencie, potem po drugim.
        literals_k = sorted(list(item_tid_lists_k.keys()))

        for i in range(len(literals_k)):
            for j in range(i + 1, len(literals_k)):
                literal_i = literals_k[i]
                literal_j = literals_k[j]

                # Dla k=1, nasze "itemy" to pojedyncze krotki. Tworzymy z nich frozenset.
                if k == 1:
                    # Sprawdzamy, czy nie próbujemy połączyć tego samego itemu z samym sobą
                    # (np. {'32', '+'} i {'32', '-'}) - taka reguła jest bez sensu.
                    if literal_i[0] == literal_j[0]:
                        continue
                    candidate = frozenset([literal_i, literal_j])
                else: # k > 1, nasze "itemy" to już frozensety krotek
                    candidate = literal_i.union(literal_j)

                if len(candidate) != k + 1:
                    continue
                
                tid_list_i = item_tid_lists_k[literal_i]
                tid_list_j = item_tid_lists_k[literal_j]
                candidate_tid_list = tid_list_i.intersection(tid_list_j)

                if len(candidate_tid_list) >= min_transactions:
                    frequent_itemsets_k_plus_1[candidate] = candidate_tid_list

        if frequent_itemsets_k_plus_1:
            for itemset, tid_list in frequent_itemsets_k_plus_1.items():
                self.frequent_itemsets[itemset] = len(tid_list)
            
            self._discover_frequent_itemsets(frequent_itemsets_k_plus_1, k + 1)