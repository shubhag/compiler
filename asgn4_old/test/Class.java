public class employee{
  int a,b ;
  public int hello(int d, int c){
    a = d;
    // c = b;
    return a;
  }

}
public class Class {

    //  public static int hello(int b, int c) {
    //   int a ;
    //   return 2;
    // }

    public static void main(String[] args) {
      int a,c;
      employee abc = new employee();
      abc.b = 1;
      c = abc.b + 4;
      a = 100;
      a =abc.hello(a,c);
      System.out.println(a);
      // c = hello(a,c);
    }

}

