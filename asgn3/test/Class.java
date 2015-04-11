public class employee{
  int a,b ;
  public int hello(int d, int c){
    a = d;
    c = b;
    return 1;
  }

}
public class Class {

     public static int hello(int b, int c) {
      int a ;
      return 2;
    }

    public static void main(String[] args) {
      int a,c;
      employee abc = new employee();
      c = abc.b ;
      a =abc.hello(a,c);
      c = hello(a,c);
    }

}

