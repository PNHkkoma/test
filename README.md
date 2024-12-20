
use Illuminate\Support\Facades\Storage;
use Maatwebsite\Excel\Facades\Excel;
use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;

public function handleExcelFile()
{
    // Retrieve file from MinIO
    $filePath = 'path/to/excel-file.xlsx';
    $tempFile = Storage::disk('s3')->get($filePath);

    // Load the Excel content
    $spreadsheet = \PhpOffice\PhpSpreadsheet\IOFactory::loadFromString($tempFile);

    // Modify the content as needed
    $sheet = $spreadsheet->g
    $sheet->setCellValue('A1', 'Modified Content');

    // Save the modified file to a temporary location
    $writer = new Xlsx($spreadsheet);
    $tempPath = storage_path('app/temp-file.xlsx');
    $writer->save($tempPath);

    // Return the modified file for download
    return response()->download($tempPath)-
    
    
    
    
    >deleteFileAfterSend(true);
}





https://id.tableau.com/token/825a6830a5b04f5abe10e0d065b0447d
