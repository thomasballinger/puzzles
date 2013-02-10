#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>
 
#define MAX_CANDIDATES 25000
#define TWOTOTHE32 4294967296
 
int64_t random64bit(){
  // we need 64 bits of random data
  int64_t r = 0;
  r += rand();
  r <<= 31;
  r += rand();
  r <<= 31;
  r += rand();
  return r;
}
 
int64_t *rand_array(long length){
  int64_t *a;
  a = malloc(sizeof(*a) * length);
  for (long i = 0; i<length; i++){
    a[i] = random64bit();
  }
  return a;
}
 
int64_t *rand_array_with_dup(long length){
  int64_t *a = rand_array(length);
  a[1234] = a[56789];
  return a;
}
 
int compare_function(const int64_t *a, const int64_t *b){
  if (*a < *b){
    return -1;
  }
  if (*a == *b){
    printf("duplicate found: it's %lld!\n", *a);
    return 0;
  }
  return 1;
}
 
int main(){
  srand(time(0));
  int length = 10000000;
  //int64_t *a = rand_array(length);
  int64_t *a = rand_array_with_dup(length);
 
  printf("Done generating random array of 64-bit ints of length %d\n", length);
  time_t now;
  time(&now);
  printf("%s", ctime(&now));
 
  uint32_t *halves = (uint32_t*) a;
  char *seen_halves = calloc(TWOTOTHE32, sizeof(char));
 
  printf("first pass\n"); fflush(stdout);
  long doublelength = length * 2;
  for (long i = 0; i<doublelength; i+=2){
    seen_halves[halves[i]] += 1;
  }
 
  int64_t candidates[MAX_CANDIDATES];
  int candidate_index = 0;
 
  printf("second pass\n"); fflush(stdout);
  for (long i = 0; i<doublelength; i+=2){
    if (seen_halves[halves[i]] > 1){
      candidates[candidate_index++] = a[i/2];
    }
  }
  printf("found %d possible duplicates, sorting now\n", candidate_index); fflush(stdout);
  qsort(candidates, candidate_index, sizeof(int64_t), compare_function);
 
  time(&now);
  printf("%s", ctime(&now)); fflush(stdout);
  return 0;
}
