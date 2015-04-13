public class fib {

	public static int fib(int n) {
        int x;
        int y;
        int z;
    if(n <= 1) {
        return n;
    } else {

        x = fib(n-1);
        y = fib(n-2);
        z = x+y;
        return z;
    }
	}
    public static void main(String[] args) {
        int i,ans;
        for(i=0;i<10;i++){
    	// int n = 4;
           ans = fib(i);
        	System.out.println(ans);
        }
}
}