import math

class Moora(object):
    alternatif = None
    kriteria = ["Harga", "Kondisi", "Rating"]
    tipe = ["cost", "benefit", "benefit"]
    jarak = [20, 10]
    bobot = [5, 3, 3]
    alternatifKriteria = None

    def setData(self, seller, criteria):
        self.alternatif = seller
        self.alternatifKriteria = criteria
        print(self.alternatifKriteria)
        return

    normalisasiKriteria = []

    def normalizationCriteria(self):
        for i in range(len(self.alternatif)):
            self.normalisasiKriteria.append([])
            for j in range(len(self.kriteria)):
                self.normalisasiKriteria[i].append(0)
                self.normalisasiKriteria[i][j] = ((max(self.jarak) - min(self.jarak)) / (
                        max([_[j] for _ in self.alternatifKriteria]) - min(
                    [_[j] for _ in self.alternatifKriteria]))) * (self.alternatifKriteria[i][j] - min(
                    [_[j] for _ in self.alternatifKriteria])) + min(self.jarak)

        print("normalisasi: ", str(self.normalisasiKriteria))
        return self.normalisasiKriteria

    pembagi = []

    def setDivider(self):
        for i in range(len(self.kriteria)):
            self.pembagi.append(0)
            for j in range(len(self.alternatif)):
                self.pembagi[i] = self.pembagi[i] + math.pow(self.normalisasiKriteria[j][i], 2)
            self.pembagi[i] = math.sqrt(self.pembagi[i])

        print("pembagi: ", str(self.pembagi))
        return self.pembagi

    normalisasiMoora = []

    def normalizationMoora(self):
        for i in range(len(self.alternatif)):
            self.normalisasiMoora.append([])
            for j in range(len(self.kriteria)):
                self.normalisasiMoora[i].append(0)
                self.normalisasiMoora[i][j] = self.normalisasiKriteria[i][j] / self.pembagi[j]

        print("normalisasi moora: ", str(self.normalisasiMoora))
        return self.normalisasiMoora

    optimasiYi = []

    def optimationYi(self):
        for i in range(len(self.alternatif)):
            self.optimasiYi.append(0)
            for j in range(len(self.kriteria)):
                if self.tipe[j] == "cost":
                    self.optimasiYi[i] = self.optimasiYi[i] - (self.normalisasiMoora[i][j] * self.bobot[j])
                else:
                    self.optimasiYi[i] = self.optimasiYi[i] + (self.normalisasiMoora[i][j] * self.bobot[j])

        print("optimasi Yi: ", str(self.optimasiYi))
        return self.optimasiYi


    alternatifRanking = []
    yiRangking = []

    def setRanking(self):
        for i in range(len(self.alternatif)):
            self.yiRangking.append(self.optimasiYi[i])
            self.alternatifRanking.append(self.alternatif[i])
        return

    def countRanking(self):
        for i in range(len(self.alternatif)):
            for j in range(len(self.alternatif)):
                if j > i:
                    if self.yiRangking[j] > self.yiRangking[i]:
                        targetYi = self.yiRangking[i]
                        targetAlternatif = self.alternatifRanking[i]
                        self.yiRangking[i] = self.yiRangking[j]
                        self.alternatifRanking[i] = self.alternatifRanking[j]
                        self.yiRangking[j] = targetYi
                        self.alternatifRanking[j] = targetAlternatif

        print("alternatif ranking: ", str(self.alternatifRanking))
        return

    def getRankScore(self):
        return self.yiRangking

    def getRanking(self):
        return self.alternatifRanking
