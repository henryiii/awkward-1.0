// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

#define FILENAME(line) FILENAME_FOR_EXCEPTIONS_CUDA("src/cpu-kernels/awkward_IndexedArray_getitem_nextcarry.cu", line)

#include "standard_parallel_algorithms.h"
#include "awkward/kernels.h"

template <typename C, typename T>
__global__
void awkward_IndexedArray_getitem_nextcarry_kernel(
    T* tocarry,
    const C* fromindex,
    int64_t* prefixedsum_mask,
    int64_t lenindex,
    int64_t lencontent,
    unsigned long long* error_i) {
  /**
   * Here the thread_id has a unsigned long long data type rather than a int64_t
   * type because atomicMin doesn't provide a fucntion signature for int64_t type
   */
  unsigned long long thread_id = blockIdx.x * blockDim.x + threadIdx.x;

  if (thread_id < lenindex) {
    C j = fromindex[thread_id];
    if (j < 0 || j >= lencontent) {
      atomicMin(error_i, thread_id);
    } else {
      tocarry[prefixedsum_mask[thread_id] - 1] = j;
    }
  }
}

template <typename C>
__global__ void
awkward_IndexedArray_getitem_nextcarry_filter_mask(
  const C* fromindex,
  int8_t* filtered_mask,
  int64_t lenindex,
  int64_t lencontent) {
  int64_t thread_id = blockIdx.x * blockDim.x + threadIdx.x;
  if (thread_id < lenindex) {
    if (!(fromindex[thread_id] < 0 || fromindex[thread_id] >= lencontent)) {
      {
        filtered_mask[thread_id] = 1;
      }
    }
  }
}

__global__ void
awkward_IndexedArray_getitem_nextcarry_initialize_error_i(
  unsigned long long* error_i,
  unsigned long long value) {
  *error_i = value;
}

template <typename C, typename T>
ERROR awkward_IndexedArray_getitem_nextcarry(
  T* tocarry,
  const C* fromindex,
  int64_t lenindex,
  int64_t lencontent) {

  dim3 blocks_per_grid = blocks(lenindex);
  dim3 threads_per_block = threads(lenindex);

  int8_t* filtered_mask;
  int64_t* res_temp;

  HANDLE_ERROR(cudaMalloc((void**)&filtered_mask, sizeof(int8_t) * lenindex));
  HANDLE_ERROR(cudaMalloc((void**)&res_temp, sizeof(int64_t) * lenindex));
  HANDLE_ERROR(cudaMemset(filtered_mask, 0, sizeof(int8_t) * lenindex));

  awkward_IndexedArray_getitem_nextcarry_filter_mask<C><<<blocks_per_grid, threads_per_block>>>(
    fromindex,
    filtered_mask,
    lenindex,
    lencontent);

  exclusive_scan(res_temp, filtered_mask, lenindex);

  unsigned long long * dev_error_i;
  unsigned long long error_i;

  HANDLE_ERROR(cudaMalloc((void**)&dev_error_i, sizeof(unsigned long long)));
  awkward_IndexedArray_getitem_nextcarry_initialize_error_i<<<1,1>>>(
    dev_error_i,
    lenindex + 1);

  awkward_IndexedArray_getitem_nextcarry_kernel<C, T><<<blocks_per_grid, threads_per_block>>>(
    tocarry,
    fromindex,
    res_temp,
    lenindex,
    lencontent,
    dev_error_i);

  HANDLE_ERROR(cudaMemcpy(&error_i, dev_error_i, sizeof(unsigned long long), cudaMemcpyDeviceToHost));

  if(error_i != lenindex + 1) {
    C error_j;
    HANDLE_ERROR(cudaMemcpy(&error_j, fromindex + error_i, sizeof(C), cudaMemcpyDeviceToHost));
    return failure("index out of range", error_i, error_j, FILENAME(__LINE__));
  }

  return success();
}
ERROR awkward_IndexedArray32_getitem_nextcarry_64(
    int64_t* tocarry,
    const int32_t* fromindex,
    int64_t lenindex,
    int64_t lencontent) {
  return awkward_IndexedArray_getitem_nextcarry<int32_t, int64_t>(
      tocarry,
      fromindex,
      lenindex,
      lencontent);
}
ERROR awkward_IndexedArrayU32_getitem_nextcarry_64(
    int64_t* tocarry,
    const uint32_t* fromindex,
    int64_t lenindex,
    int64_t lencontent) {
  return awkward_IndexedArray_getitem_nextcarry<uint32_t, int64_t>(
      tocarry,
      fromindex,
      lenindex,
      lencontent);
}
ERROR awkward_IndexedArray64_getitem_nextcarry_64(
    int64_t* tocarry,
    const int64_t* fromindex,
    int64_t lenindex,
    int64_t lencontent) {
  return awkward_IndexedArray_getitem_nextcarry<int64_t, int64_t>(
      tocarry,
      fromindex,
      lenindex,
      lencontent);
}
