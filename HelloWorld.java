import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class X {
    public boolean insertPrIssue(String pr, String issue, String projName) {
        // Assuming you have a DBUtil class with a method getConnection(dbcon, user, pswd)
        Connection con = DBUtil.getConnection(dbcon, user, pswd);
        int count = 0;
        try {
            Statement comandoSql = con.createStatement();
            // Make sure to use PreparedStatement to prevent SQL injection
            String sql = "INSERT INTO pr_issue (pr, issue, projName) VALUES (?, ?, ?)";
            // Use PreparedStatement to safely insert values
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, pr);
            pstmt.setString(2, issue);
            pstmt.setString(3, projName);

            count = pstmt.executeUpdate();
            // Close the PreparedStatement after use
            pstmt.close();
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        } finally {
            // Close the connection in finally block to ensure it's always closed
            try {
                if (con != null) {
                    con.close();
                }
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }

        // Return true if at least one row was affected, false otherwise
        return count > 0;
    }
}
