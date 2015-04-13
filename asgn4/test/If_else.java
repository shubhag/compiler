class If_else {
    public static void main(String[] args) {
    	int x = 30;
    	int y = 10;

    	if( x == 30 ){
            int a;
    		if( y == 10 ){
    			System.out.println(y);
    		}
    	}
    	x = 30;

    	if( x < 20 ){
    		System.out.println(y);
    	}else{
    		System.out.println(x);
    	}
    	int z;
		z = (x > y) ? x : y;
        System.out.println(z);
    }
}