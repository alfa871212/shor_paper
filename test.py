from qiskit.visualization import plot_histogram
new_dict={}
res={'1 0 0 0 0 0 0 0': 240, '0 1 0 0 0 0 0 0': 277, '1 1 0 0 0 0 0 0': 246, '0 0 0 0 0 0 0 0': 261}
for iter in list(res):

    tmp = iter
    tmp=tmp.replace(" ",'')
    #print(tmp)
    new_dict[tmp]=res.pop(iter)
    
   
print(new_dict)
plot_histogram(new_dict,figsize=(10,10),title=f'N={15} a={2} result(Seq)').savefig('test.png')
