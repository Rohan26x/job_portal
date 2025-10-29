'use client';

import { useState, useEffect } from 'react';
import { jobSeekerAPI } from '@/lib/api';
import { useAuth } from '@/context/AuthContext';
import styles from './Profile.module.css';

export default function JobSeekerProfilePage() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    bio: '',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await jobSeekerAPI.getMyProfile();
      setProfile(response.data);
      setFormData({
        first_name: response.data.first_name || '',
        last_name: response.data.last_name || '',
        bio: response.data.bio || '',
      });
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');

    try {
      await jobSeekerAPI.updateProfile(formData);
      setMessage('Profile updated successfully!');
      setIsEditing(false);
      fetchProfile();
    } catch (error) {
      console.error('Error updating profile:', error);
      setMessage('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setFormData({
      first_name: profile.first_name || '',
      last_name: profile.last_name || '',
      bio: profile.bio || '',
    });
  };

  if (loading) {
    return <div className={styles.loading}>Loading profile...</div>;
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>My Profile</h1>

      <div className={styles.profileCard}>
        <div className={styles.section}>
          <h2>Account Information</h2>
          <div className={styles.infoRow}>
            <span className={styles.label}>Email:</span>
            <span className={styles.value}>{user?.email}</span>
          </div>
          <div className={styles.infoRow}>
            <span className={styles.label}>User Type:</span>
            <span className={styles.value}>Job Seeker</span>
          </div>
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader}>
            <h2>Personal Information</h2>
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className={styles.editBtn}
              >
                Edit Profile
              </button>
            )}
          </div>

          {message && (
            <div className={message.includes('success') ? styles.success : styles.error}>
              {message}
            </div>
          )}

          {isEditing ? (
            <div className={styles.form}>
              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label htmlFor="first_name">First Name</label>
                  <input
                    type="text"
                    id="first_name"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    disabled={saving}
                  />
                </div>

                <div className={styles.formGroup}>
                  <label htmlFor="last_name">Last Name</label>
                  <input
                    type="text"
                    id="last_name"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    disabled={saving}
                  />
                </div>
              </div>

              <div className={styles.formGroup}>
                <label htmlFor="bio">Bio</label>
                <textarea
                  id="bio"
                  name="bio"
                  value={formData.bio}
                  onChange={handleChange}
                  rows="6"
                  disabled={saving}
                />
              </div>

              <div className={styles.actions}>
                <button
                  onClick={handleCancel}
                  className={styles.cancelBtn}
                  disabled={saving}
                >
                  Cancel
                </button>
                <button
                  onClick={handleSave}
                  className={styles.saveBtn}
                  disabled={saving}
                >
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </div>
          ) : (
            <div>
              <div className={styles.infoRow}>
                <span className={styles.label}>First Name:</span>
                <span className={styles.value}>
                  {profile?.first_name || 'Not provided'}
                </span>
              </div>
              <div className={styles.infoRow}>
                <span className={styles.label}>Last Name:</span>
                <span className={styles.value}>
                  {profile?.last_name || 'Not provided'}
                </span>
              </div>
              <div className={styles.infoRow}>
                <span className={styles.label}>Bio:</span>
                <span className={styles.value}>
                  {profile?.bio || 'Not provided'}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
