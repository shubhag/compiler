public class Switch {

    public static void main(String[] args) {
        char grade = 'D';
        // int grade = 4
        switch(grade)
        {
         case 'A' :
            System.out.println(1); 
            break;
         case 'B' :
         case 'C' :
            System.out.println(2);
            break;
         case 'D' :
            System.out.println(3);
         case 'F' :
            System.out.println(4);
            break;
         default :
            System.out.println(5);
        }
}
}