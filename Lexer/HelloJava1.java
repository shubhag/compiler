//file: HelloJava1.java
public class HelloJava1 extends javax.swing.JComponent {
public static void main(String[] args) {
javax.swing.JFrame f = new javax.swing.JFrame("HelloJava1");
f.setSize(300, 300);
f.getContentPane().add(new HelloJava1( ));
f.setVisible(true);
char a = 'a';
float a = 0b1000_0000_0000_0000_0000_0000_0000_0000l;
}
public void paintComponent(java.awt.Graphics g) {
g.drawString("Hello, Java!", 125, 95);
}
}