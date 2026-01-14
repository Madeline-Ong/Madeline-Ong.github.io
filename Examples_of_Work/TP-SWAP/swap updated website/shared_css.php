<!-- AUTHOR: MADELINE ONG YING XUAN -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: STYLING FOR THE PAGES IN THE HR WEBSITE THAT DISPLAYS INFORMATION -->

<style>
.button_container {
    margin-top: 40px;
    display: flex;
    gap: 20px;
    justify-content: center;
}
.container {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 0 50px;
}
.table_container {
	padding-left: 50px;
	padding-right: 50px;
	margin-bottom: 10px;
}
.button {
	padding: 10px 20px;
	text-decoration: none;
	border: none;
	border-radius: 5px;
	font-size: 16px;
	color: #fff;
	background-color: #007bff;
	transition: background-color 0.3s ease;
}
.button:hover {
	background-color: #0056b3;
}
table {
	border-collapse: collapse;
	width: 100%;
	margin: 20px auto;
}
th, td {
	border: 1px solid #ddd;
	padding: 8px;
	text-align: left;
}
th {
	background-color: #f2f2f2;
}
tr:nth-child(even) {
	background-color: #f9f9f9;
}
.modal {
	display: none;
	position: fixed;
	z-index: 1;
	padding-top: 100px;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	overflow: auto;
	background-color: rgb(0, 0, 0);
	background-color: rgba(0, 0, 0, 0.4);
}
.modal_content {
	background-color: #fefefe;
	margin: auto;
	padding: 20px;
	border: 1px solid #888;
	width: 80%;
}
</style>
