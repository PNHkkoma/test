itms-services://?action=download-manifest&url=https%3A%2F%2Fviettelfamily.com%2Fuploads%2Fviettel360%2Fvops%2Fios%2FvOps.plist

https://www.figma.com/design/UUhBgaK92cgYvvmLmcHmEo/QLH%C4%90_v3_%C4%91%C3%A1nh-s%E1%BB%91?m=auto&t=IndL3BmHleiFKCE0-6



https://www.figma.com/design/R8Hk8WcGLjn78KUDDnpHmj/UX_PVN?m=auto&t=UxmdAmGHfwE7tYQR-1
m=auto&t=UxmdAmGHfwE7tYQR-1
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
