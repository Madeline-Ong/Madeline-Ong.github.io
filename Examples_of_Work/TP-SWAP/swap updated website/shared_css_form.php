<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: STYLING FOR THE FORMS IN THE HR WEBSITE -->
<style>
body {
	margin: 0;
	font-family: Arial, sans-serif;
}
.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	background-color: #333;
	color: #fff;
	padding: 20px;
}
form {
	max-width: 400px;
	margin: 20px auto 0;
	background-color: #fff;
	padding: 20px;
	border-radius: 8px;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
label {
	display: block;
	margin-bottom: 8px;
}
input[type="date"], input[type='text'], input[type='password'] {
	width: calc(100% - 22px); 
	padding: 10px;
	margin-bottom: 15px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
}
button[type="submit"] {
	padding : 10px;
	margin-bottom: 15px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
	font-size: 16px;
	background-color: #007bff;
	color: #fff;
	border: none;
	cursor: pointer;
	padding: 10px;
}

button[type="submit"]:hover {
	background-color: #0056b3;
}
</style>
