"""
A simple implementation of GTP 2 Tokenizer

"""

class Tokenizer:
    def __init__(self) -> None:
        self.VOCALSIZE = 1000
        self.NUM_MERGES = self.VOCALSIZE - 256
        self.merges = {}
        self.vocab = self._build_vocab()
        self.version = "1.0"
        self.identifier = "ember"

    def _get_stats(self,ids):
        # This internal method will gwt the pairs with higesting repeting number 
     count = {}
     for pair in zip(ids,ids[1:]): #type : ignore
        count[pair] = count.get(pair,0)+1
     return count

    
    def _build_vocab(self):
        # this method will build voal for visual apperance 
        vocab = {idx:bytes([idx]) for idx in range(256)}
        for (p0,p1),idx in self.merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]

        return vocab
    
    def merge(self,ids,pair,idx):
     # this method will merge pairs into new idx (token)
     newids = []
     i = 0 
     while i<len(ids):
        if i <len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
            newids.append(idx)
            i +=2
        else:
            newids.append(ids[i])
            i +=1
     return newids

    def encode(self,text:str):
        # encodes string 
        tokens = list(text.encode("utf-8"))
        while len(tokens) >=2:
            stats = self._get_stats(tokens)
            pair = min(stats,key=lambda p: self.merges.get(p,float("inf")))
            if pair not in self.merges:
                break
            idx = self.merges[pair]
            tokens  = self.merge(tokens,pair,idx)

        return tokens

    def decode(self,ids):
        #dedcodes token into string 
        tokens = b"".join(self.vocab[idx] for idx in ids)

        text = tokens.decode("utf-8",errors="replace") 
        return text

    def save(self):
        # this method will sabve the tokenizer once trained 
        with open (f"{self.identifier}.tokenizer","w") as f :
            f.write(f"{self.identifier} | {self.version} \n")
            f.write(f"{self.VOCALSIZE} \n")
            for (p0,p1),idx in self.merges.items():
                f.writelines(f"{p0} {p1} \n")


    def load(self,tokenizer):
        # this method will load the tokenizer 
        assert tokenizer.endswith("tokenizer")
        merges = {} 
        with open(tokenizer,"r",encoding="utf-8") as f:
            identifer = f.readline().strip()
            self.vocab=  int(f.readline().strip())
            idx = 256
            for line in f:
                p0,p1 = map(int,line.split())
                merges[(p0,p1)] = idx
                idx +=1
            self.merges = merges
            self.vocab = self._build_vocab()
    

    def train(self,ids:list):
        """ 
        This method wil train the tokenizer .
        It will crash if the trainning data is huge , use small data for Learning purpose only . 
        for effective trainning ther is another training function.
        """
        for i in range(self.NUM_MERGES): 
         stats = self._get_stats(ids)
         if not stats: 
          print(f"Stopped early at merge {i}, no more pairs to merge")
          return
         pair = max(stats,key=lambda k: stats[k])
         idx = 256 + i 
         ids = self.merge(ids,pair,idx)
         self.merges[pair] = idx
        self.vocab = self._build_vocab()
        return self.merges



