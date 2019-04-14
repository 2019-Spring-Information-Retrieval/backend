from inverted_index import Index

class SeqSearchWord(object):
    def __init__(self, status=True):
        self.arg = arg
        if status: # 只有 词语的模式
            self.model = self._readModel()
        else: # 同时有词语和词性的模式 （未实现）
            self.model = self._readModel()

    def _readModel(self):

        # 固定
        model.eval()
        return model

    def output(qwords):
        # 保证swords 是 List[str]型数据
        # 如果输出只有word，可以直接使用倒排档的index
        swords = self.model(qword_in).item()
        return Index.search(swords)

    
