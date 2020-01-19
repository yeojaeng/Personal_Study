## SQLI - statement & prepared statement

---



| 구분                   | 내용                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **Statement**          | 외부 입력값이 쿼리값에 직접 삽입되는 구조 -> 취약<br />String data1 = "외부 입력값1"<br />String data2 = "외부 입력값2"<br />String sql = "insert into member values('"+data1+"', '"+data2+"); |
| **Prepared Statement** | 위와는 다르게 직접적으로 변수를 지정하지 않고, `?`로 표시하는 바인드 형태의 변수를 사용한다.<br />또한, 입력값은 `setXXX`형태로 설정하여 입력을 처리하기 때문에 쿼리구조가 사전 컴파일된다.<br />즉, 외부의 악의적 입력값에도 쿼리구조는 변경되지 않기 때문에 `statement`방식에 비하여 안전한다.<br /><br />PreparedStatement pstmt = con.prepareStatement(sql);<br />String sql = insert into member values(?,?)<br />pstmt.setString(1, data1);<br />pstmt.setString(2, data2); |



### 코드 예시

---

#### Statement 방식

```java
String query = "SELECT * FROM user_data WHERE last_name = '" + accountNmae + "'";
ec.addElement(new PRE(query));

try
{
    Statement statement = connection.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,
	ResultSet.CONCUR_READ_ONLY);
    ResultSet results = statement.executeQuery(query);
}
```

`Line 6`에서 `Statement`방식을 통해 쿼리를 생성한다.



#### Prepared Statement 방식

```java
String query = "SELECT * FROM user_data WHERE last_name = ?";
ec.addElement(new PRE(query));

try
{
    PreparedStatement statement = connection.prepareStatement(query, 			 	    ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
	statement.setString(1, accountName);
    ResultSet results = statement.executeQuery(query);
}
```

`Line 6`에서 `PreparedStatement`방식을 채택했다.

또한, `statement`의 데이터 또한 `setXXX`방식을 통해 데이터를 초기화한다.





