class If_else {
    public static void main(String[] args) {
    	int x = 30;
    	int y = 10;

    	if( x == 30 ){
    		if( y == 10 ){
    			System.out.println("X = 30 and Y = 10");
    		}
    	}
    	x = 30;

    	if( x < 20 ){
    		System.out.println("This is if statement");
    	}else{
    		System.out.println("This is else statement");
    	}
    	int z;
		z = (x < y) ? x : y;
    }
}