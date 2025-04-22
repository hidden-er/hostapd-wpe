def log2hashcat():
	cnt = 0
	hashes = {}
	with open('hostapd-wpe.log', 'r') as f:
		while True:
			line = f.readline()
			if line == '':
				break
			if line.startswith('mschapv2:'):
				username = ''
				hashcatvalue = ''
				while True:
					line = f.readline().strip()
					if line == '':
						break
					elif line.startswith('username:'):
						username = line[len('username:'):].strip()
					elif line.startswith('hashcat NETNTLM:'):
						hashcatvalue = line[len('hashcat NETNTLM:'):].strip()
						cnt += 1
				if username not in hashes:
					hashes[username] = hashcatvalue
	print("mschapv2 number: {}".format(cnt))
	print("non-duplicative mschapv2 number: {}".format(len(hashes)))

	#hashes.txt本身可能还存在未爆破的哈希;hostapd-wpe.log中提取的应当添加而不是覆盖
	with open('hashes.txt', 'a') as f:
		for value in hashes.values():
			f.write(value + '\n')

def hashcat2netntlm():
	with open('hashes.txt', 'r') as fin:
		with open('netntlm.txt', 'w') as fout:
			for line in fin:
				hashvalue = line.strip()
				split = hashvalue.split(':')
				ntresp = split[-2]
				challenge = split[-1]
				fout.write('$NETNTLM$' + challenge + '$' + ntresp + '\n')


def remove_duplicate_hashes():
	existing_student_ids = set()
	with open('all_hashes.txt', 'r') as f:
		for line in f:
			student_id = line.strip().split('::::')[0]
			existing_student_ids.add(student_id)

	cnt = 0
	filtered_lines = []
	with open('hashes.txt', 'r') as f:
		for line in f:
			current_line = line.strip()
			current_student_id = current_line.split('::::')[0]
			cnt += 1
			if current_student_id not in existing_student_ids and current_student_id not in filtered_lines:
				filtered_lines.append(line)
				student_id = line.strip().split('::::')[0]
				existing_student_ids.add(student_id)

	print("hashes number: {}".format(cnt))
	print("non-duplicative hashes number: {}".format(len(filtered_lines)))

	#去重,必须覆盖
	with open('hashes.txt', 'w') as f:
		f.writelines(filtered_lines)

if __name__ == '__main__':
	log2hashcat()
	hashcat2netntlm()
	remove_duplicate_hashes()