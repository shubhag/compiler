class array {
    public static void main(String[] args) {
       int[] ia = new int[101];
       for (int i = 0; i < 101; i++) 
        {
       		ia[i] = i;
       	}
       int sum = 0;
       int j;
       for (j = 0;j< 101;j++) {
       	sum += ia[j];
       }
       System.out.println(sum);

    }
}
