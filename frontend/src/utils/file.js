export const validateResumeFile = (file) => {
  if (file.size > 10 * 1024 * 1024) {
    return { valid: false, message: 'File size exceeds 10MB limit.' };
  }
  const allowedTypes = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword'
  ];
  const fileExt = file.name.toLowerCase().slice(file.name.lastIndexOf('.'));
  if (!allowedTypes.includes(file.type) && !['.pdf', '.docx', '.doc'].includes(fileExt)) {
    return { valid: false, message: 'Please upload a PDF or DOCX file.' };
  }
  return { valid: true, message: '' };
};
