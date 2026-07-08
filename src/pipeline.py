import extract
import transform
import load


print("\n---------------Ectract proccess have started---------------")
extract.run()
print("Ectract seasons proccess have ended")

print('\n---------------Transforming process started---------------')
transform.run()
print('Transforming process finished')

print('\n---------------Loading  process started---------------')
load.run()
print('Loading  process finished')

