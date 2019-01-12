import socket
import multiprocessing
import re
import dynamic.mini_frame


class Web_server(object):
	def __init__(self):

		# 1.创建一个套接字
		self.tcp_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# 防止出问题后，浏览器出现堵塞
		self.tcp_socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		# 2.绑定本地信息
		self.tcp_socket_server.bind(("", 7890))
		
		# 3.改套接字为监听
		self.tcp_socket_server.listen(128)

	def __del__(self):
		# 关闭服务器套接字
		self.tcp_socket_server.close()

	def client_server(self, new_socket):
		# 接受数据
		recv_data = new_socket.recv(1024).decode("utf-8")
		lines = recv_data.splitlines()
		# print(lines)
		ret = re.match(r"[^/]*(/[^ ]*)", lines[0])
		if ret:
			file_name = ret.group(1)
			if file_name == "/":
				file_name = "/index.py"
		else:
			return
			
		print(file_name)
		# 动态页面请求判断	
		if not file_name.endswith(".py"):
			# 静态资源
			try:
				f = open("./static" + file_name, "rb")
			except:
				print("-----4--------")
				header = "HTTP/1.1 404 NOT FOUND\r\n"
				header += "\r\n"
				f = open("./static/error.html", "rb")
				f_error = f.read()
				f.close()
				response = header.encode("utf-8") + f_error 
				new_socket.send(response)
			else:
				print("-----5--------")
				# 发送数据给客户端
				body = f.read()
				f.close()
				header = "HTTP/1.1 200 OK\r\n"
				header += "\r\n"
				response = header.encode("utf-8") + body 
				new_socket.send(response)
		else:
			print("----------6-----------")
			env = dict()  # 传参字典	
			print("----------6.1-----------")
			env['PATH_INFO'] = file_name
			print("----------6.2-----------")
			body = dynamic.mini_frame.application(env, self.set_response_header) 
			print("----------7-----------")
			header = "HTTP/1.1 %s\r\n" % self.status

			for temp in self.headers:
				header += "%s%s\r\n" % (temp[0], temp[1])

			header += "\r\n"
			print("----------8-----------")
			response = header.encode("utf-8") + body
			new_socket.send(response)
				
		# 关闭客服端套接字
		new_socket.close()

	def set_response_header(self, status, header):
		self.status = status
		self.headers = [("server", "mini_web v1.0")]
		self.headers += header

	def run(self):

		while True:
			"""创建多进程,多任务web服务器"""

			print("------1-------")
			# 4.等待客户端的链接
			new_socket, client_addr = self.tcp_socket_server.accept()
			# 5.为客户端服务
			p = multiprocessing.Process(target=self.client_server, args=(new_socket,))
			p.start()
			# self.client_server(new_socket)
			# 6.退出套接字 
			new_socket.close()



def main():

	# 创建一个实例对象
	web_server = Web_server()
	web_server.run()
	


if __name__ == "__main__":
	main()
