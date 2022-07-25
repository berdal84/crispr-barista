
class Fastq:

    # Split a multiread file to two single read files.
    @staticmethod
    def split_r1r2( in_path, out_r1_path, out_r2_path):

        r1 = open(out_r1_path,'w+')
        r2 = open(out_r2_path,'w+')

        if  not r1 or not r2:
            return False
        
        for i, line in enumerate(open(in_path)):
            if i % 8 < 4:
                r1.write(line)
            else:
                r2.write(line)

        r1.close()
        r2.close()
        return True

