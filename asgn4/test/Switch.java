public class Switch {

    public static void main(String[] args) {
        int fruits = 6;
        // int grade = 4
        switch(fruits)
        {
         case 1 :
            System.out.println("Only 1 fruit"); 
            break;
         case 2 :
            System.out.println("Two fruits");
            break;
         case 3 :
            System.out.println("Three fruits");
            break;
         case 4 :
            System.out.println("Four fruits");
            break;
         case 5 :
            System.out.println("Great! Five fruits");
            break;
         default :
            System.out.println("Not sure how many fruits are there");
        }
}
}