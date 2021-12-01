//========================================================================
// ubmark-quicksort
//========================================================================
// This version (v1) is brought over directly from Fall 15.

#include "common.h"
#include "ubmark-quicksort.dat"
#include <stdio.h>

//------------------------------------------------------------------------
// quicksort-scalar
//------------------------------------------------------------------------

void swap(int* x, int* y) {
  int temp = *x;
  *x = *y;
  *y = temp;
} 

int partition(int* src, int begin, int end) {
  int idx = begin; // To iterate through the array for swapping
  int pivot = src[end-1];

  if (end < begin){
    return end;
  }
  
  if ( begin == end) {
    return idx;
  }

  for (int i = idx; i <end; i++ ) {
    if ( src[i] <= pivot) {
      swap(&src[i],&src[idx]);
      idx++;
      } 
    }
 

  return idx-1;
}

void qsort(int* src, int begin, int end) {

  if (begin >= end) {
    return; 
  }

  int idx = partition(src,begin,end); // index of the partition
  qsort(src,begin,idx); // recursive case for one half of the array
  qsort(src,idx+2,end); // recursive case for other half of the array 

}

__attribute__ ((noinline))
void quicksort_scalar( int* dest, int* src, int size )
{

    // implement quicksort algorithm here
    qsort(src,0,size);   

    int i;
    // dummy copy src into dest
    for ( i = 0; i < size; i++ ){
      dest[i] = src[i];
      printf("%d, ", dest[i]);
    }
    printf("\n\n");
}

//------------------------------------------------------------------------
// verify_results
//------------------------------------------------------------------------

void verify_results( int dest[], int ref[], int size )
{
  int i;

  for ( i = 0; i < size; i++ ) {
    
    if ( !( dest[i] == ref[i] ) ) {
      test_fail( i, dest[i], ref[i] );
    }
  }
  test_pass();
}

//------------------------------------------------------------------------
// Test Harness
//------------------------------------------------------------------------

int main( int argc, char* argv[] )
{
  int dest[size];

  int i;
  for ( i = 0; i < size; i++ )
    dest[i] = 0;

  test_stats_on();
  quicksort_scalar( dest, src, size );
  test_stats_off();

  verify_results( dest, ref, size );

  return 0;
}
