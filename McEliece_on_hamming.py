import numpy as np
import random

#Деление элементов вектора по модюлю 2
def mod_on_2(vector):
	div_vector = vector.copy()
	div_vector.fill(2)
	return np.remainder(vector, div_vector)

#Обращение бита с заданным индексом в матрице
def reverse_bit(vector, index):
	if index == 0:
		return vector
	if vector[0, index-1] == 1:
		vector[0, index-1] = 0
	else:
		vector[0, index-1] = 1
	return vector

#--------------------- Класс расшифровывания криптосистемы Мак-Элиса ---------------------#
class DecryptMcEliece:
	#Параметры кода Хэмминга (7, 4):
	n = 7
	k = 4
	G = np.matrix([
		[0,1,1,1,0,0,0],
		[1,0,1,0,1,0,0],
		[1,1,0,0,0,1,0],
		[1,1,1,0,0,0,1]
		], dtype=int
	)
	H = np.matrix([
		[1,0,0,0,1,1,1],
		[0,1,0,1,0,1,1],
		[0,0,1,1,1,0,1]
		], dtype=int
	)
	S = []
	P = []
	
	#Конструктор, запускающий генерацию матриц S и P
	def __init__(self):
		self.S = self.matrix_gen_S()
		self.P = self.matrix_gen_P()

	#Генерация случайной невырожденной матрицы S
	def matrix_gen_S(self):
		while True:
			matrixS = np.random.randint(0, 2, (self.k, self.k), "int")
			if np.linalg.det(matrixS) % 2 == 1:
				return np.matrix(matrixS, dtype="int")

	#Генерация матрицы перестановки P
	def matrix_gen_P(self):
		matrixP = []
		indexes = np.random.permutation(self.n)
		for index in indexes:
			matrixP.append([1 if i == index else 0 for i in range(self.n)])
		return np.matrix(matrixP, dtype="int")

	#Вывод закрытого ключа
	def print_privateKey(self):
		print ("Невырожденная матрица S: \n" + str(self.S) + "\n")
		print ("Подстановочная матрица P: \n" + str(self.P) + "\n")

	#Создание открытой ключа
	def make_matrixSGP(self):
		pub_key = mod_on_2(self.S*self.G*self.P)
		return pub_key

	#Расшифровка закодированного слова
	def decrypt(self, cod):
		uSGe = mod_on_2(cod * mod_on_2(self.P.I.astype(int)))
		sindrom = mod_on_2(self.H * uSGe.T)
		e = self.search_error(sindrom)
		uSG = reverse_bit(uSGe, e)
		uS = uSG[0, 3:self.k+3]
		return mod_on_2(uS * mod_on_2(self.S.I.astype(int)))

	#Расшифровка файла
	def decryptFile(self, file_name):
		dec_file = open(file_name, "rb")
		dec_bits = np.array([])
		bytes = np.fromfile(dec_file, dtype = "uint8")
		bits = np.unpackbits(bytes)
		
		if bits.size % self.n > 0:
			while bits.size % self.n != 0:
				bits = np.append(bits, 0)
		for i in range(0, bits.size-1, self.n):
			seq = bits[i:i+self.n]
			dec = self.decrypt(seq)
			if i == 0:
				dec_bits = dec
			else:
				dec_bits = np.vstack((dec_bits, dec))
		
		ebc_bytes = np.packbits(dec_bits)
		ebc_bytes.tofile("Decrypt " + file_name)
		dec_file.close()
		
	#Поиск позиции ошибки расшифровке
	def search_error(self, sindrom):
		T_H = self.H.T.tolist()
		T_sindrom = sindrom.T.tolist()[0]
		
		#В случае если синдром содержит только нули ошибки нет
		no_error = False
		zero_num = 0
		for x in T_sindrom:
			if x == 0:
				zero_num += 1
		if zero_num == len(T_sindrom):
			no_error = True
		#Если ошибки нет, то возвращаем 0, в остальных случаях возвращаем позицию ошибки
		if no_error:
			return 0
		else:
			return T_H.index(T_sindrom) + 1

#--------------------- Класс шифрования криптосистемы Мак-Элиса ---------------------#
class EncryptMcEliece:
	matrixSGP = []
	n = 0
	k = 0
	
	#Чтение параметров из переданного открытого ключа
	def __init__(self, matrixSGP):
		self.matrixSGP = matrixSGP
		self.k = matrixSGP.shape[0] #длина исходного слова
		self.n = matrixSGP.shape[1] #Длина кодового слова

	#Вывод открытого ключа
	def print_publicKey(self):
		print ("Матрица открытого ключа: \n" + str(self.matrixSGP) + "\n")

	#Шифрование кодового слова
	def encrypt(self, u):
		matrix_e = np.zeros((1,self.n), dtype=int)
		e = random.randint(1, self.n)
		matrix_e = reverse_bit(matrix_e, e)
		cod = mod_on_2(u * self.matrixSGP)
		cod = mod_on_2(cod + matrix_e)
		return cod

	#Шифрование файла
	def encryptFile(self,file_name):
		sr_file = open(file_name, "rb")
		enc_bits = np.array([])
		bytes = np.fromfile(sr_file, dtype = "uint8")
		bits = np.unpackbits(bytes)
		
		if bits.size % self.k > 0:
			while bits.size % self.k != 0:
				np.append(bits, 0)
		for i in range(0, bits.size-1, self.k):
			seq = bits[i:i+self.k]
			enc = self.encrypt(seq)
			if i == 0:
				enc_bits = enc
			else:
				enc_bits = np.vstack((enc_bits, enc))
		
		ebc_bytes = np.packbits(enc_bits)
		ebc_bytes.tofile("Encrypt " + file_name)
		sr_file.close()

#Основное тело программы
if __name__ == "__main__":
	subscriber_A = DecryptMcEliece()
	subscriber_B = EncryptMcEliece(subscriber_A.make_matrixSGP())
	subscriber_B.print_publicKey()
	print ("Шифрование файла: 'Файл.txt'\n")
	subscriber_B.encryptFile("Файл.txt")
	print("Вывод закрытого ключа:\n")
	subscriber_A.print_privateKey()
	print ("Расшифрование файла: 'Encrypt Файл.txt'")
	subscriber_A.decryptFile("Encrypt Файл.txt")