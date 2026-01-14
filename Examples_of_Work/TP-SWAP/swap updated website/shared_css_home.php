<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: STYLING FOR THE HOMEPAGES IN THE HR WEBSITE -->

<style>
body {
	margin: 0;
	font-family: Arial, sans-serif;
}
header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	background-color: #333;
	color: #fff;
	padding: 20px;
}
.container {
	display: flex;
	overflow-x: auto;
	justify-content: center;
	padding: 20px;
	scrollbar-width: none;
	-ms-overflow-style: none;
}
.container::-webkit-scrollbar {
	display: none;
}
.block {
	width: 400px;
	height: 300px;
	background-color: #f9f9f9;
	border: 1px solid #ddd;
	padding: 20px;
	margin: 15px;
	border-radius: 5px;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}
.block img {
	max-width: 200px;
	max-height: 200px;
	border-radius: 5px;
}
h2 {
	margin-top: 0;
	color: #333;
}
</style>
